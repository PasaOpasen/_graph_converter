
from pathlib import Path

from conv.main import conv


def main():
    for f in sorted(Path('inputs').glob('*.json')):
        print(f"processing {f}")
        conv(
            str(f), f"outputs/{f.stem}.yaml"
        )


if __name__ == '__main__':
    # conv(
    #     'inputs/ЛПНП.json',
    #     'tmp.yml'
    # )
    main()
