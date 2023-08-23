
from typing import Dict, Tuple, Sequence, List, Callable, Any

import re


def fix_string_name(s: str) -> str:
    """
    fixes string to correct python name

    >>> _ = fix_string_name
    >>> _('a')
    'a'
    >>> _('a b.c-e')
    'a_b_c_e'
    """
    return s.replace(' ', '_').replace('-', '_').replace('.', '_').strip()


def name_to_tree_call(s: str) -> str:
    """
    >>> name_to_tree_call('name')
    '___{{ name }}'
    """
    # return f"___{sum(ord(_s) for _s in s)}"
    return "___{{ " + s + " }}"


#region JINJA VARIABLES

_var_pattern = re.compile(r"\{\{\s[^\{}]*\s}}")


def get_string_vars(s: str) -> Dict[Tuple[int, int], str]:
    """
    seeks for all {{ }} variables in the string
    Args:
        s:

    Returns:
        dict { (start, end) -> variable name } where end is not included

    >>> get_string_vars('{{ a }}  {{ bb }}')
    {(0, 7): 'a', (9, 17): 'bb'}
    """
    return {
        (m.start(), m.end()): s[m.start(): m.end()].strip('{ }')
        for m in _var_pattern.finditer(s)
    }


def replace_string_vars(s: str, name_resolver: Callable[[str], Any]) -> str:
    """
    replaces jinja vars in the string
    Args:
        s:
        name_resolver: function returns variables values for variables names

    Returns:
        new string

    >>> _ = replace_string_vars
    >>> variables = dict(a=1, b=2, c=3)
    >>> resolver = variables.get
    >>> assert _(s='', name_resolver=resolver) == ''
    >>> assert _('no vars', resolver) == 'no vars'
    >>> _('{{ a }} + {{ b }} == {{ c }}', resolver)
    '1 + 2 == 3'
    """
    if not s:
        return s

    vars_data = get_string_vars(s)
    if not vars_data:
        return s

    all_vars = set(vars_data.values())
    var2val = {
        v: str(name_resolver(v))
        for v in all_vars
    }

    s = list(s)
    for (start, end), name in sorted(vars_data.items(), reverse=True):
        s[start:end] = list(
            var2val[name]
        )

    return ''.join(s)

#endregion


def add_numbers_to_sorted(seq: Sequence, sep: str = '.') -> List[str]:
    """
    adds numbers to names to keep them in sorted order
    Args:
        seq:
        sep:

    Returns:

    >>> _ = add_numbers_to_sorted
    >>> _([1, 2, 3])
    ['1.1', '2.2', '3.3']
    >>> _((1, 2), sep='|')
    ['1|1', '2|2']
    >>> _(list(range(12)))
    ['01.0', '02.1', '03.2', '04.3', '05.4', '06.5', '07.6', '08.7', '09.8', '10.9', '11.10', '12.11']
    """

    count = len(seq)
    count = len(str(count))

    return [
        f"{str(i).rjust(count, '0')}{sep}{v}"
        for i, v in enumerate(seq, 1)
    ]









