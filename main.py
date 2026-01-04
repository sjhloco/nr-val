import argparse

import yaml
from nornir import InitNornir
from nornir_validate import (
    generate_val_file,
    print_result_gvf,
    print_result_val,
    validate,
)


def main() -> None:
    # Setup nornir inventory
    nr = InitNornir(config_file="config.yml")
    # Runtime arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--validation", action="store_true")
    parser.add_argument("-g", "--gen_val_file", action="store_true")
    parser.add_argument(
        "data_file", nargs="?", default="input_data.yml", help="Input file"
    )
    args = parser.parse_args()

    # ----------------------------------------------------------------------------
    # LOAD: Load files used by the script
    # ----------------------------------------------------------------------------
    # Uses input_data.yml if none specified at runtime (only for validate)
    try:
        with open(args.data_file) as tmp_data:
            input_data = yaml.load(tmp_data, Loader=yaml.Loader)
    ## VAL_DATA: If file doesn't exist uses raw validation data
    except FileNotFoundError:
        input_data = {
            "groups": {
                "ios": {
                    "intf_bonded": {
                        "port_channel": {
                            "Po1": {"protocol": "LACP", "members": ["Gi0/2", "Gi0/3"]}
                        }
                    },
                }
            }
        }

    # ----------------------------------------------------------------------------
    # Generate Validation file: Examples of creating validation files with the differing options
    # ----------------------------------------------------------------------------
    if args.gen_val_file:
        ### No user defined input index file, uses nornir-validate full list of indexes
        if args.data_file == "input_data.yml":
            result = nr.run(task=generate_val_file)
        ### With input index file, save validation files in current location
        else:
            result = nr.run(task=generate_val_file, input_data=input_data)
            ## To save validation files in a specific directory
            # result = nr.run(
            #     task=val_file_builder,
            #     input_data=input_data,
            #     directory="/Users/ste/Desktop/nr-val/val_files",
            # )

        ### PRINT: Normal print
        print_result_gvf(result, nr)
        ## Enable to print errors in val file build (output of failed netmiko commands)
        # from nornir_rich.functions import print_result
        # print_result(result)

    # ----------------------------------------------------------------------------
    # Validation: Examples of doing validation with the differing options
    # ----------------------------------------------------------------------------
    elif args.validation:
        ### RUN: To run with either of the inputs, will always print the compliance report
        result = nr.run(task=validate, input_data=input_data, print_report=True)
        ## Only prints compliance report if fails
        # result = nr.run(task=validate, input_data=input_data)
        ### Report: Save the report to file, specifiy a directory or use "" for the current direcfory
        # result = nr.run(task=validate, input_data=input_data, save_report="")

        ### PRINT: Uses my custom nornir.rich print
        print_result_val(result)


if __name__ == "__main__":
    main()
