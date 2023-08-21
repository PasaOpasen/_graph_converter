
#region IMPORTS

from typing import Dict, Union, Set, Tuple, List, Literal, Sequence

from pathlib import Path
from dataclasses import dataclass, field

from .utils import read_json, dumps_yaml, write_text, mkdir_of_file

from .types.input import JsonInput, LinkModel, NodeModel, BranchingModel, OperatorModel, AnalysesInput
from .types.output import YamlTree, YamlNormalNode, YamlStatusNode

#endregion


def _replace_spaces(s: str) -> str:
    return s.replace(' ', '_')


def get_port_ends(name: str, edges: Dict[str, LinkModel]) -> List[str]:
    """returns labels of the entities which are connected by edges with are connected to this port"""
    res = []

    is_in = is_out = False
    """flags about whether the arg port is input or output"""

    for edge in edges.values():
        if edge['sourcePort'] == name:
            res.append(edge['target'])
            is_in = True
        elif edge['targetPort'] == name:
            res.append(edge['source'])
            is_out = True

        # if is_in and is_out:
        #     raise ValueError(f"{name} port is used as input and output port both!")

    return res


@dataclass
class Condition:
    data: BranchingModel
    analyses: AnalysesInput
    nodes: Dict[str, NodeModel]
    edges: Dict[str, LinkModel]

    links_condition: Set[str] = field(default_factory=set)
    """links to the model itself and its input params"""
    links_true: Set[str] = field(default_factory=set)
    links_false: Set[str] = field(default_factory=set)
    ops: List[Tuple[str, str, str]] = field(default_factory=list)

    def __post_init__(self):
        for p in self.data['ports']:
            i = p['id']
            n = p['name']
            if n.endswith('true'):
                self.links_true.add(i)
            elif n.endswith('false'):
                self.links_false.add(i)
            else:
                self.links_condition.add(i)
        self._fill()

    def _expand1(self, name: Literal['true', 'false', 'condition']) -> List[str]:
        """adds direct inputs and outputs nodes to links"""
        port = next((p for p in self.data['ports'] if p['name'].endswith(name)), None)['id']
        assert port, f'no {name} port'
        entities = get_port_ends(port, self.edges)
        assert entities, f"nothing connected to {name} port"
        getattr(self, f"links_{name}").update(entities)
        return entities

    def _op_process(self, operator: str):

        model: OperatorModel = self.nodes[operator]
        left_ports = [p for p in model['ports'] if p['alignment'] == 'left']
        assert len(left_ports) == 2, left_ports

        words = []
        for p in left_ports:
            entities = get_port_ends(p['id'], self.edges)
            assert len(entities) == 1, entities
            ent = entities[0]
            self.links_condition.add(ent)
            words.append(ent)

        left, right = words
        if self.nodes[left]['type'] == 'data':  # change order to ensure the parameter will be at left
            right, left = left, right

        self.ops.append(
            (left, operator, right)
        )

    def _fill(self):

        self._expand1('false')
        self._expand1('true')
        ops = self._expand1('condition')

        assert all(self.nodes[op]['type'] == 'operator' for op in ops), ops

        for op in ops:
            self._op_process(op)

    @staticmethod
    def expand(conditions: Sequence['Condition']):
        """add primary condition link to close conditions"""
        for i, c1 in enumerate(conditions):
            for j, c2 in enumerate(conditions):
                if i == j:
                    continue

                c2_id = c2.data['id']
                if c1.links_true.intersection(c2.links_condition):
                    c1.links_true.add(c2_id)
                if c1.links_false.intersection(c2.links_condition):
                    c1.links_false.add(c2_id)


    def get_code(self, true_counts: int, false_counts: int) -> str:
        lines = []
        for left, op, right in self.ops:
            tp = self.nodes[left]['type']

            _left = _replace_spaces(self.analyses[left])
            _left = (
                _left if tp == 'parameter' else f"___{_left}____"
            )

            lines.append(
                _left + ' ' + ' '.join(
                    _replace_spaces(self.analyses[k])
                    for k in (op, right)
                )
            )

        if len(lines) == 1:
            expr = lines[0]
        else:
            expr = ' and '.join(f"({e})" for e in lines)

        if true_counts == false_counts == 1:
            return expr

        #
        # use yields shits
        #

        lines = [f"$expr {expr}"]

        e = f"{expr} == True"
        lines.extend(
            [f'yield {e}'] * (true_counts - 1)
        )
        lines.append(e)

        e = f"{expr} == False"
        lines.extend(
            [f'yield {e}'] * (false_counts - 1)
        )
        lines.append(e)

        return '\n'.join(lines)

    def as_node(self, hash2number: Dict[str, int]) -> YamlNormalNode:
        res = dict(
            children='',
            code=''
        )

        true_results = sorted(
            set(
                hash2number[h] for h in self.links_true
                if h in hash2number
            )
        )
        assert true_results
        false_results = sorted(
            set(
                hash2number[h] for h in self.links_false
                if h in hash2number
            )
        )
        assert false_results

        res['code'] = self.get_code(len(true_results), len(false_results))
        res['children'] = ' '.join(
            str(i) for i in (true_results + false_results + [false_results[-1]])
        )

        return res


def conv_dict(d: JsonInput) -> Dict[int, Union[YamlNormalNode, YamlStatusNode]]:

    contents = d['analyses']

    _edges, _nodes = d['diagramData']['layers']

    edges: Dict[str, LinkModel] = _edges['models']
    nodes: Dict[str, NodeModel] = _nodes['models']

    conditions: List[Condition] = []
    all_ins: Set[str] = set()
    """ids of input models of all conditions"""
    for n in nodes.values():
        if n['type'] == 'branching':
            c = Condition(n, edges=edges, nodes=nodes, analyses=contents)
            conditions.append(c)
            all_ins.update(c.links_condition)

    outputs = [
        n for n in nodes.values()
        if n['id'] not in all_ins and n['type'] in ('analyse', 'result')
    ]

    assert outputs, 'no output nodes'

    Condition.expand(conditions)

    hash2number = {
        c.data['id']: i
        for i, c in enumerate(conditions, 1)
    }
    """string hash to node id"""
    hash2number.update(
        {n['id']: len(hash2number) + i for i, n in enumerate(outputs, 1)}
    )

    result = {}
    for i, c in enumerate(conditions, 1):
        result[i] = c.as_node(hash2number)

    for i, n in enumerate(outputs, 1):
        cont = contents[n['id']]
        result[len(hash2number) + i] = dict(
            code=(
                f"___{_replace_spaces(cont)}"
                if n['type'] == 'analyse'
                else f".res {cont['title']}"
            )
        )

    return result


def conv(js_path: str, yaml_path: str):

    dct = read_json(js_path)
    f_name = _replace_spaces(Path(js_path).stem)

    d = conv_dict(dct)

    yaml_tree: YamlTree = dict(
        nodes=d,
        user=0,
        tag='',
        description=f_name,
        name=f_name,
        statuses={'none': 'none'}
    )

    y = dumps_yaml(yaml_tree)
    mkdir_of_file(yaml_path)
    write_text(yaml_path, y)




