
from typing import TypedDict, Dict, Union


class TreeMeta(TypedDict):
    """metadata for each analysis (all data except nodes)"""
    user: int
    name: str
    tag: str
    description: str

    statuses: Dict[str, str]
    """map of statuses descriptions: {status -> description}"""


class YamlChildren(TypedDict):
    """children structure in yaml file"""
    cases: Union[int, str]
    """nodes for cases as string like '1 2 3', int whether only one case"""
    default: int
    """default node"""


class YamlStatusNode(TypedDict):
    """
    status node

    provides only code, no children futher
    """
    code: str
    """expression with '\n' support instead of ';' (but not requires)"""


class YamlNormalNode(YamlStatusNode):
    """
    non-status node

    in fact: status + children
    """
    children: Union[str, YamlChildren]


class YamlTree(TreeMeta):
    """yaml file structure"""

    nodes: Dict[int, Union[YamlNormalNode, YamlStatusNode]]
    """{id -> node config}"""


