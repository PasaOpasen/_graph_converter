
from typing import Dict, Any, TypedDict, Union, Literal, List, Tuple

import sys

if sys.version_info.minor < 10:
    from typing_extensions import TypeAlias
else:
    from typing import TypeAlias


class StatusNodeContent(TypedDict):
    title: str
    description: str


class LinkModel(TypedDict):
    id: str
    source: str
    sourcePort: str
    target: str
    targetPort: str


#region NODE MODELS

class _NodePort(TypedDict):
    id: str
    parentNode: str
    # name: str
    in_: bool
    """in json it is 'in'"""
    links: List[str]
    alignment: Literal['left', 'right']


class _NodeModel(TypedDict):
    id: str
    # type: str
    # ports: List[_NodePort]


class PortParameter(_NodePort):
    name: Literal['Parameter-in-port', 'Parameter-out-port']


class ParameterModel(_NodeModel):
    type: Literal['parameter']
    ports: List[PortParameter]


class PortData(_NodePort):
    name: Literal['data-out-blue']


class DataModel(_NodeModel):
    type: Literal['data']
    ports: List[PortData]


class PortAnalyse(_NodePort):
    name: Literal['Analyse-in-port', 'Analyse-out-port']


class AnalyseModel(_NodeModel):
    type: Literal['analyse']
    ports: List[PortAnalyse]


class PortOperator(_NodePort):
    name: Literal['operator-out-blue', 'operator-in-blue', 'operator-in-red']


class OperatorModel(_NodeModel):
    type: Literal['operator']
    ports: List[PortOperator]


class PortBranching(_NodePort):
    name: Literal['branching-out-true', 'branching-out-false', 'branching-in-condition']


class BranchingModel(_NodeModel):
    type: Literal['branching']
    ports: List[PortBranching]


class PortResult(_NodePort):
    name: Literal['result-in-port']


class ResultModel(_NodeModel):
    type: Literal['result']
    ports: List[PortResult]


NodeModel: TypeAlias = Union[ParameterModel, DataModel, OperatorModel, BranchingModel, ResultModel]

#endregion


class JsonLayerLink(TypedDict):
    type: Literal['diagram-links']
    models: Dict[str, LinkModel]


class JsonLayerNode(TypedDict):
    type: Literal['diagram-nodes']
    models: Dict[str, NodeModel]


class DiagramData(TypedDict):
    layers: Tuple[JsonLayerLink, JsonLayerNode]


AnalysesInput: TypeAlias = Dict[str, Union[str, StatusNodeContent]]


class JsonInput(TypedDict):
    analyses: AnalysesInput
    diagramData: DiagramData
