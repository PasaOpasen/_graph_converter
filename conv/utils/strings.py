

def fix_string_name(s: str) -> str:
    """
    fixes string to correct python name

    >>> _ = fix_string_name
    >>> _('a')
    'a'
    >>> _('a b.c-e')
    'a_b_c_e'
    """
    return s.replace(' ', '_').replace('-', '_').replace('.', '_')


def name_to_tree_call(s: str) -> str:
    """
    >>> name_to_tree_call('name')
    '___{{ name }}'
    """
    # return f"___{sum(ord(_s) for _s in s)}"
    return "___{{ " + s + " }}"
