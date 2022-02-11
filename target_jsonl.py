#!/usr/bin/env python3

import argparse
import io
import simplejson as json
import os
import sys
from datetime import datetime

import singer
from jsonschema import Draft4Validator, FormatChecker
from adjust_precision_for_schema import adjust_decimal_precision_for_schema

logger = singer.get_logger()


def emit_state(state):
    if state is not None:
        line = json.dumps(state)
        logger.debug('Emitting state {}'.format(line))
        sys.stdout.write("{}\n".format(line))
        sys.stdout.flush()



def persist_messages(
    messages,
    destination_path,
    custom_name=None,
    do_timestamp_file=True
):
    state = None
    schemas = {}
    key_properties = {}
    validators = {}

    timestamp_file_part = '-' + datetime.now().strftime('%Y%m%dT%H%M%S') if do_timestamp_file else ''

    for message in messages:
        try:
            o = singer.parse_message(message).asdict()
        except json.decoder.JSONDecodeError:
            logger.error("Unable to parse:\n{}".format(message))
            raise
        message_type = o['type']
        if message_type == 'RECORD':
            if o['stream'] not in schemas:
                raise Exception(
                    "A record for stream {}"
                    "was encountered before a corresponding schema".format(o['stream'])
                )

            validators[o['stream']].validate((o['record']))

            filename = (custom_name or o['stream']) + timestamp_file_part + '.jsonl'
            filename = os.path.expanduser(os.path.join(destination_path, filename))

            with open(filename, 'a', encoding='utf-8') as json_file:
                json_file.write(json.dumps(o['record']) + '\n')

            state = None
        elif message_type == 'STATE':
            logger.debug('Setting state to {}'.format(o['value']))
            state = o['value']
        elif message_type == 'SCHEMA':
            stream = o['stream']
            schemas[stream] = o['schema']
            adjust_decimal_precision_for_schema(schemas[stream])
            validators[stream] = Draft4Validator((o['schema']))
            key_properties[stream] = o['key_properties']
        else:
            logger.warning("Unknown message type {} in message {}".format(o['type'], o))

    return state


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='Config file')
    args = parser.parse_args()

    if args.config:
        with open(args.config) as input_json:
            config = json.load(input_json)
    else:
        config = {}

    input_messages = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    state = persist_messages(
        input_messages,
        config.get('destination_path', ''),
        config.get('custom_name', ''),
        config.get('do_timestamp_file', True)
    )

    emit_state(state)
    logger.debug("Exiting normally")


if __name__ == '__main__':
    main()
