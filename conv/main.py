
#region IMPORTS

from typing import Dict, Any, Set, Tuple, List, Literal

from dataclasses import dataclass, field

from .utils import read_json, dumps_yaml, write_text, mkdir_of_file

from .types.input import JsonInput, LinkModel, NodeModel, BranchingModel

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
            res.append(edge['source'])
            is_in = True
        elif edge['targetPort'] == name:
            res.append(edge['target'])
            is_out = True

        if is_in and is_out:
            raise ValueError(f"{name} port is used as input and output port both!")

    return res


@dataclass
class Condition:
    data: BranchingModel
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

    def _fill(self):

        def expand1(name: Literal['true', 'false', 'condition']) -> List[str]:
            port = next((p for p in self.data['ports'] if p['name'].endswith(name)), None)['id']
            assert port, f'no {name} port'
            entities = get_port_ends(port, self.edges)
            assert entities, f"nothing connected to {name} port"
            getattr(self, f"links_{name}").update(entities)
            return entities

        expand1('false')
        expand1('true')
        ops = expand1('condition')

        print()







def conv_dict(d: JsonInput) -> Dict[str, Any]:

    contents = d['analyses']

    _edges, _nodes = d['diagramData']['layers']

    edges: Dict[str, LinkModel] = _edges['models']
    nodes: Dict[str, NodeModel] = _nodes['models']

    conditions: List[Condition] = []
    for n in nodes.values():
        if n['type'] == 'branching':
            c = Condition(n, edges=edges, nodes=nodes)
            conditions.append(c)



    return d


def conv(js_path: str, yaml_path: str):

    dct = read_json(js_path)

    d = conv_dict(dct)

    y = dumps_yaml(d)
    mkdir_of_file(yaml_path)
    write_text(yaml_path, y)




