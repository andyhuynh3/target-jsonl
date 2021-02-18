# target-jsonl

A [Singer](https://singer.io) target that writes data to JSONL ([JSON Lines](http://jsonlines.org/)) files.

## How to use it

`target-jsonl` works together with any other [Singer Tap] to move data from sources like [Braintree], [Freshdesk] and [Hubspot] to JSONL formatted files.

### Install

We will use [`tap-exchangeratesapi`][Exchangeratesapi] to pull currency exchange rate data from a public data set as an example.

First, make sure Python 3 is installed on your system or follow these installation instructions for [Mac] or [Ubuntu].

It is recommended to install each Tap and Target in a separate Python virtual environment to avoid conflicting dependencies between any Taps and Targets.

```bash
 # Install tap-exchangeratesapi in its own virtualenv
python3 -m venv ~/.virtualenvs/tap-exchangeratesapi
source ~/.virtualenvs/tap-exchangeratesapi/bin/activate
pip install tap-exchangeratesapi
deactivate

# Install target-jsonl in its own virtualenv
python3 -m venv ~/.virtualenvs/target-jsonl
source ~/.virtualenvs/target-jsonl/bin/activate
pip install target-jsonl
deactivate
```

### Run

We can now run `tap-exchangeratesapi` and pipe the output to `target-jsonl`.

```bash
~/.virtualenvs/tap-exchangeratesapi/bin/tap-exchangeratesapi | ~/.virtualenvs/target-jsonl/bin/target-jsonl
```

The data by default will be written to a file called `exchange_rate-{timestamp}.jsonl` in your working directory.

```bash
› cat exchange_rate-{timestamp}.jsonl
{"CAD": 1.3954067515, "HKD": 7.7503228187, "ISK": 147.1130787678, "PHP": 50.5100534957, "DKK": 6.8779745434, "HUF": 327.9376498801, "CZK": 25.018446781, "GBP": 0.8059214167, "RON": 4.4673491976, "SEK": 9.9002029146, "IDR": 15321.0016602103, "INR": 75.6516325401, "BRL": 5.4711307877, "RUB": 73.6220254566, "HRK": 6.9765725881, "JPY": 106.548607268, "THB": 32.420217672, "CHF": 0.9750046117, "EUR": 0.9223390518, "MYR": 4.3475373547, "BGN": 1.8039107176, "TRY": 6.988286294, "CNY": 7.0764619074, "NOK": 10.3973436635, "NZD": 1.6446227633, "ZAR": 18.4316546763, "USD": 1.0, "MXN": 24.1217487548, "SGD": 1.4152370411, "AUD": 1.5361556908, "ILS": 3.5102379635, "KRW": 1218.9540675152, "PLN": 4.1912931194, "date": "2020-04-29T00:00:00Z"}
```

### Optional Configuration

`target-jsonl` takes an optional configuration file that can be used to set formatting parameters like the delimiter - see [config.sample.json](config.sample.json) for examples. To run `target-jsonl` with the configuration file, use this command:

```bash
~/.virtualenvs/tap-exchangeratesapi/bin/tap-exchangeratesapi | ~/.virtualenvs/target-jsonl/bin/target-jsonl -c my-config.json
```

Here is a brief description of the optional config keys

`destination_path` - Specifies where to write the resulting `.jsonl` file to. By default, the file gets written in your working directory.

`custom_name` - Specifies a custom name for the filename, instead of the stream name (i.e. `{custom_name}-{timestamp}.jsonl`, asumming `do_timestamp_file` is `true`). By default, the stream name will be used.

`do_timestamp_file` - specifies if the file should get timestamped. By default, the resulting file will have a timestamp in the file name (i.e. `exchange_rate-{timestamp}.jsonl` as described above in the `Run` section). If this option gets set to `false`, the resulting file will not have a timestamp associated with it (i.e. `exchange_rate.jsonl` in our example).

---

Copyright &copy; 2020 Andy Huynh

[Singer Tap]: https://singer.io
[Braintree]: https://github.com/singer-io/tap-braintree
[Freshdesk]: https://github.com/singer-io/tap-freshdesk
[Hubspot]: https://github.com/singer-io/tap-hubspot
[Exchangeratesapi]: https://github.com/singer-io/tap-exchangeratesapi
[Mac]: http://docs.python-guide.org/en/latest/starting/install3/osx/
[Ubuntu]: https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-ubuntu-16-04