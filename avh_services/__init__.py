from os import PathLike
import re
import typing
from collections.abc import Iterator


def read_json(path: PathLike, start: str, end: str) -> Iterator[dict[str, typing.Any]]:
    with open(path, encoding="utf-8", errors='ignore') as file:
        content = file.read()
        content = content.replace('\\\\"', "{899}")
        row = {}
        for match in re.finditer(r'"(\w+)"\s*:\s*(-?\d+(?:\.\d+)?|null|".*?")', content):
            if match[1] == start:
                row = {}
            row[match[1]] = eval("None" if match[2] == "null" else match[2].replace(
                '{899}', '\\"').replace("\\\\r", "\\r"))
            if match[1] == end:
                yield row
