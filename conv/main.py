
from typing import Dict, Any, TypedDict, Union, Literal, List

from .utils import read_json, dumps_yaml, write_text, mkdir_of_file


#region TYPES

class StatusNode(TypedDict):
    title: str
    description: str


class JsonLayer(TypedDict):
    type: Literal['diagram-links', 'diagram-nodes']
    models: Dict[str, Dict[str, Any]]


class JsonInput(TypedDict):
    analyses: Dict[str, Union[str, StatusNode]]
    diagramData: List[JsonLayer]


#endregion


def _replace_spaces(s: str) -> str:
    return s.replace(' ', '_')


def conv_dict(d: JsonInput) -> Dict[str, Any]:

    contents = d['analyses']

    return d


def conv(js_path: str, yaml_path: str):

    dct = read_json(js_path)

    d = conv_dict(dct)

    y = dumps_yaml(d)
    mkdir_of_file(yaml_path)
    write_text(yaml_path, y)




