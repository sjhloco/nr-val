# nr-val

A test script for running [nornir-validate](https://github.com/sjhloco/nornir-validate) with a static Nornir inventory, see the [documentation](https://nornir-validate.readthedocs.io/en/latest/index.html) for more details on *nornir-validate*.

## Prerequisites

Clone the repository and install the required python packages, the easiest way to do this is with [uv](https://docs.astral.sh/uv/) as it automatically creates and activates the virtual environment.

```bash
git clone https://github.com/sjhloco/nr-val.git
cd nr-val/

uv sync
```

If you are using [pip](https://pypi.org/project/pip/) first create and activate the virtual environment before installing the packages.

```bash
python -m venv .venv
.\.venv\Scripts\Activate
pip install -r requirements.txt
```

## Generate Validation file

Validation files are built based on an index file ([example index files](https://github.com/sjhloco/nornir-validate/tree/main/src/nornir_validate/index_files)), if a index file is not provided the validation file will be created for all the enabled features on the device.

```bash
uv run ./main.py -g example_index.yml            # Create x_vals.yml with validations only for those in the specified index file
uv run ./main.py -g                              # Create x_vals.yml with validations for all enabled feature
```

## Compliance Report

Compliance reports can be created based on a file specified at runtime ([example validation files](https://github.com/sjhloco/nornir-validate/tree/main/example_validation_files)), the default file (*input_data.yml*) or if neither exist from raw validation data defined in *main.py*. The report will be printed to screen no matter what, this can be changed to do so for only failed reports by removing the `print_report` argument from the *validate* task (in *main.py*).

```bash
uv run ./main.py -v                         # Prints a compliance report based on validations in input_data.yml (falls back to script DM)
uv run ./main.py -v ./R1_vals.yml           # Prints a compliance report based on validations in the specified validation file (R1_vals.yml)                            
```

Add `save_report` to the *validate* task to save the report to file (*hostname_compliance_report_YYYYMMDD-HHMM.json*).
