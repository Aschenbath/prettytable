from __future__ import annotations

import io

import pytest

from prettytable import from_csv


@pytest.mark.parametrize("delimiter", [",", ";", "\t"])
def test_csv_sniffing_preserves_initial_position(delimiter: str) -> None:
    contents = delimiter.join(["name", "value"]) + "\n"
    contents += delimiter.join(["first", "1"]) + "\n"
    contents += delimiter.join(["second", "2"]) + "\n"
    stream = io.StringIO("Exported report\n" + contents)
    stream.readline()

    table = from_csv(stream)

    assert table.field_names == ["name", "value"]
    assert table.rows == [["first", "1"], ["second", "2"]]


def test_csv_sniffing_with_explicit_headers_at_offset() -> None:
    stream = io.StringIO("Exported report\nfirst,1\nsecond,2\n")
    stream.readline()

    table = from_csv(stream, field_names=["name", "value"])

    assert table.rows == [["first", "1"], ["second", "2"]]
