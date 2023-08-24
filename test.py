
from pathlib import Path

from traceback import print_exc

from conv.utils.strings import fix_string_name

from conv.main import conv
from conv.ordering import order_graphs


def main(raise_on_errors: bool = False):
    for f in sorted(Path('inputs').glob('*.json')):
        if f.stem.startswith('__'):
            continue

        print(f"processing {f}")

        def call():
            conv(
                str(f),
                f"outputs/{fix_string_name(f.stem)}.yaml"
            )

        if raise_on_errors:
            call()
        else:
            try:
                call()
            except Exception:
                print_exc()
                print(f"error {f}")

    order_graphs('outputs', 'outputs_sorted')


if __name__ == '__main__':
    # conv(
    #     'inputs/ЛПНП.json',
    #     'tmp.yml'
    # )
    main(raise_on_errors=True)
