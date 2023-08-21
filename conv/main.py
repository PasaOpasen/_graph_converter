
#region IMPORTS

from typing import Dict, Any

from dataclasses import dataclass

from .utils import read_json, dumps_yaml, write_text, mkdir_of_file

from .types.input import JsonInput, LinkModel, NodeModel

#endregion


def _replace_spaces(s: str) -> str:
    return s.replace(' ', '_')




def conv_dict(d: JsonInput) -> Dict[str, Any]:

    contents = d['analyses']

    _edges, _nodes = d['diagramData']['layers']

    edges: Dict[str, LinkModel] = _edges['models']
    nodes: Dict[str, NodeModel] = _nodes['models']


    return d


def conv(js_path: str, yaml_path: str):

    dct = read_json(js_path)

    d = conv_dict(dct)

    y = dumps_yaml(d)
    mkdir_of_file(yaml_path)
    write_text(yaml_path, y)




