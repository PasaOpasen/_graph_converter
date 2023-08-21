
from typing import Union, List, Dict, Any

import os
from pathlib import Path
import io


def read_json(path: Union[str, os.PathLike]) -> Union[Dict[str, Any], List]:
    import orjson
    return orjson.loads(
        Path(path).read_bytes()#.decode('utf-8')
    )


def save_json(path: Union[str, os.PathLike], data: Union[Dict, List, Any]):
    import orjson

    Path(path).write_bytes(
        orjson.dumps(data, option=orjson.OPT_INDENT_2 | orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_NON_STR_KEYS)
    )

    # dump = json.dumps(
    #     data.asdict() if hasattr(data, 'asdict') else data,
    #     ensure_ascii=False,
    #     indent=2
    # )
    # result_tmp = str(path)
    # Path(result_tmp).write_bytes(dump.encode('utf-8', 'ignore'))


def write_text(result_path: Union[str, os.PathLike], text: str, encoding: str = 'utf-8'):
    result_tmp = str(result_path) + '.tmp'
    Path(result_tmp).write_text(text, encoding=encoding, errors='ignore')
    if os.path.exists(result_path):
        os.remove(result_path)
    Path(result_tmp).rename(result_path)


def read_text(result_path: Union[str, os.PathLike], encoding: str = 'utf-8'):
    return Path(result_path).read_text(encoding=encoding, errors='ignore')


def write_pickle(result_path: str, data: Any):
    import pickle
    dump = pickle.dumps(data)  # , protocol=4)
    result_tmp = str(result_path) + '.tmp'
    Path(result_tmp).write_bytes(dump)
    if os.path.exists(result_path):
        os.remove(result_path)
    Path(result_tmp).rename(result_path)


def read_pickle(result_path: str):
    import pickle
    data = pickle.loads(Path(result_path).read_bytes())
    return data


def dumps_yaml(dct: Dict[str, Any]):
    """
    converts dictionary to yaml format string

    >>> print(dumps_yaml(dict(a=1, b=2, c='abc', d={'a': [1, 2], 'b': (1, 2), 'c': {1: 1, 2: 2}})).strip())
    a: 1
    b: 2
    c: abc
    d:
      a:
      - 1
      - 2
      b: !!python/tuple
      - 1
      - 2
      c:
        1: 1
        2: 2
    """
    import yaml
    return yaml.dump(dct, encoding='utf-8', allow_unicode=True).decode()


def parse_yaml(
    source: Union[str, io.StringIO]
) -> Dict[str, Any]:
    """
    reads dict from .yaml file or string io

    >>> dct = {'a': 1, 'b': [1, 2, 3], 'c': {0: 0, 1: 1}}
    >>> s = dumps_yaml(dct)
    >>> assert parse_yaml(io.StringIO(s)) == dct
    """
    import yaml
    if isinstance(source, str):
        with open(source, 'r', encoding='utf-8') as f:
            file_configs = yaml.safe_load(f)
    else:
        file_configs = yaml.safe_load(source)
    return file_configs

