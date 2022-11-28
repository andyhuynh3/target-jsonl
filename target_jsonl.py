#!/usr/bin/env python3

import argparse
import io
import os
import sys
from datetime import datetime
from pathlib import Path

import jsonschema
import simplejson as json
import singer
from adjust_precision_for_schema import adjust_decimal_precision_for_schema

logger = singer.get_logger()

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", help="Config file")


def emit_state(state):
    if state is not None:
        line = json.dumps(state)
        logger.debug(f"Emitting state {line}")
        sys.stdout.write(f"{line}\n")
        sys.stdout.flush()


def create_stream_file_handler(destination_path, filename):
    Path(destination_path).mkdir(parents=True, exist_ok=True)
    filename = os.path.expanduser(os.path.join(destination_path, filename))
    return open(filename, "a", encoding="utf-8")


def persist_messages(
    messages, destination_path="./", custom_name=None, do_timestamp_file=True, raw=False
):
    state = None
    schemas = {}
    key_properties = {}
    validators = {}
    stream_file_handles = {}

    timestamp_file_part = (
        "-" + datetime.now().strftime("%Y%m%dT%H%M%S") if do_timestamp_file else ""
    )

    try:
        if raw:
            filename = (custom_name or "target_jsonl") + timestamp_file_part + ".jsonl"
            stream_file_handles["raw"] = create_stream_file_handler(
                destination_path=destination_path, filename=filename
            )

        for message in messages:
            try:
                o = singer.parse_message(message).asdict()
            except json.decoder.JSONDecodeError:
                logger.error(f"Unable to parse:\n{message}")
                raise

            message_type = o["type"]
            if message_type in {"RECORD", "SCHEMA"}:
                stream = o["stream"]

            if message_type == "RECORD":
                if o["stream"] not in schemas:
                    raise Exception(
                        f"A record for stream {stream} was encountered before a corresponding schema"
                    )

                try:
                    validators[o["stream"]].validate((o["record"]))
                except jsonschema.ValidationError as e:
                    logger.error(
                        f"Failed parsing the json schema for stream: {stream}."
                    )
                    raise e

                if not raw:
                    handler = stream_file_handles.get(stream)
                    handler.write(json.dumps(o["record"]) + "\n")

                state = None

            elif message_type == "STATE":
                logger.debug(f'Setting state to {o["value"]}')
                state = o["value"]

            elif message_type == "SCHEMA":
                schemas[stream] = o["schema"]
                adjust_decimal_precision_for_schema(schemas[stream])
                validators[stream] = jsonschema.Draft4Validator((o["schema"]))
                key_properties[stream] = o["key_properties"]
                if not raw:
                    filename = (custom_name or stream) + timestamp_file_part + ".jsonl"
                    stream_file_handles[stream] = create_stream_file_handler(
                        destination_path=destination_path, filename=filename
                    )

            else:
                logger.warning(f"Unknown message type {message_type} in message {o}")

            if raw:
                handler = stream_file_handles.get("raw")
                handler.write(message)
    finally:
        for handler in stream_file_handles.values():
            handler.close()
    return state


def main(args=None):
    args = parser.parse_args(args)

    if args.config:
        with open(args.config) as input_json:
            config = json.load(input_json)
    else:
        config = {}

    input_messages = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")
    state = persist_messages(
        input_messages,
        config.get("destination_path", "./"),
        config.get("custom_name"),
        config.get("do_timestamp_file", True),
        config.get("raw", False),
    )

    emit_state(state)
    logger.debug("Exiting normally")


if __name__ == "__main__":
    main()
