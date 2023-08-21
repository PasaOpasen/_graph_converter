
from typing import Dict, Any

from .utils import read_json, dumps_yaml, write_text, mkdir_of_file


def conv_dict(d: Dict[str, Any]) -> Dict[str, Any]:
    return d


def conv(js_path: str, yaml_path: str):

    dct = read_json(js_path)

    d = conv_dict(dct)

    y = dumps_yaml(d)
    mkdir_of_file(yaml_path)
    write_text(yaml_path, y)




