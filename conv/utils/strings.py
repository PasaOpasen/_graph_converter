

def fix_string_name(s: str) -> str:
    return s.replace(' ', '_').replace('-', '_').replace('.', '_')


def name_to_tree_call(s: str) -> str:
    # return f"___{sum(ord(_s) for _s in s)}"
    return "___{{ " + s + " }}"
