import io
import os
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

import pytest

from target_jsonl import main

tests_dir = Path(os.path.dirname(os.path.abspath(__file__)))
samples_dir = tests_dir / "samples"
output_dir = tests_dir / "output"


def run_target(args=None):
    stdout_buf = io.StringIO()
    stderr_buf = io.StringIO()

    with redirect_stdout(stdout_buf), redirect_stderr(stderr_buf):
        main(args)

    stdout_buf.seek(0)
    stderr_buf.seek(0)
    return stdout_buf.read(), stderr_buf.read()


simple_stream_records = '{"id": 1, "metric": 1}\n{"id": 2, "metric": 2}\n{"id": 3, "metric": 10}\n{"id": 4, "metric": 20}\n{"id": 5, "metric": 100}\n'


def test_records(monkeypatch):
    stdin_input = (samples_dir / "simple_stream.singer").open()
    config = samples_dir / "sample_config.json"
    output_file = output_dir / "test_records.jsonl"
    if output_file.exists():
        # clean up from previous test
        os.remove(output_file)
    monkeypatch.setattr("sys.stdin", stdin_input)
    stdout, stderr = run_target(args=["--config", str(config)])
    assert stdout == '{"test_records": 5}\n'
    assert output_file.exists()
    with open(output_file, "r") as op:
        simple_stream_output = op.read()
        assert simple_stream_output == simple_stream_records


def test_records_raw(monkeypatch):
    config = samples_dir / "sample_config_raw.json"
    input_file = samples_dir / "simple_stream.singer"
    output_file = output_dir / "target_jsonl.jsonl"
    if output_file.exists():
        # clean up from previous test
        os.remove(output_file)
    monkeypatch.setattr("sys.stdin", input_file.open())
    stdout, stderr = run_target(args=["--config", str(config)])
    assert stdout == '{"test_records": 5}\n'
    assert output_file.exists()
    with open(input_file, "r") as ip, open(output_file, "r") as op:
        assert ip.read() == op.read()
