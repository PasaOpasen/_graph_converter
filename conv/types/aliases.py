
from typing import (
    Tuple, Sequence,
    Optional, Union, TypeVar, Literal
)

import sys

if sys.version_info.minor < 10:
    from typing_extensions import TypeAlias
else:
    from typing import TypeAlias

_ = TypeAlias

T = TypeVar('T')


