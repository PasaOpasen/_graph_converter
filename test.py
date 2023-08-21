
from pathlib import Path

from traceback import print_exc

from conv.main import conv


def main():
    for f in sorted(Path('inputs').glob('*.json')):
        if f.stem.startswith('__'):
            continue

        print(f"processing {f}")
        try:
            conv(
                str(f), f"outputs/{f.stem}.yaml"
            )
        except Exception:
            print_exc()
            print(f"error {f}")


if __name__ == '__main__':
    # conv(
    #     'inputs/ЛПНП.json',
    #     'tmp.yml'
    # )
    main()
