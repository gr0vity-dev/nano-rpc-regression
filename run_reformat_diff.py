import argparse
import json


def write_results_to_file(result, filename):
    with open(filename, 'w') as outfile:
        json.dump(result, outfile, indent=4)


def process_values(reformatted, change_type, main_key, key, values):
    nested_key = values['difference_on_key']

    if main_key not in reformatted[change_type]:
        reformatted[change_type][main_key] = {
            "key": nested_key,
        }

    for version_key in set(values.keys()) - {"difference_on_key"}:
        reformatted[change_type][main_key][version_key] = values[version_key]

    reformatted[change_type][main_key].setdefault("parameters", []).append(key)


def reformat_data(input_data):
    reformatted = {}

    for change_type, change_content in input_data.items():
        reformatted[change_type] = {}

        for main_key, main_values in change_content.items():
            for key, values in main_values.items():
                process_values(reformatted, change_type, main_key, key, values)

    return reformatted


def main():
    parser = argparse.ArgumentParser(
        description='Reformat and write JSON data.')
    parser.add_argument('-i', '--input', required=True, help='Input file name')
    parser.add_argument('-o',
                        '--output',
                        required=True,
                        help='Output file name')
    args = parser.parse_args()

    with open(args.input) as f1:
        data = json.load(f1)
    reformatted = reformat_data(data)

    write_results_to_file(reformatted, args.output)


if __name__ == "__main__":
    main()
