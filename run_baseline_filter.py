import argparse
import json


def generate_filter_list(base_line_diff_file):
    with open(base_line_diff_file) as f:
        base_line_diff = json.load(f)

    filter_list = []
    for change_type, changes in base_line_diff.items():
        for method, diffs in changes.items():
            for diff_key, diff_values in diffs.items():
                filter_list.append(diff_key)
    return filter_list


def filter(input_dict, keys_to_filter):
    filtered_dict = {}
    for key, value in input_dict.items():
        if key in keys_to_filter:
            continue
        if isinstance(value, dict):
            filtered_value = filter(value, keys_to_filter)
            if filtered_value:
                filtered_dict[key] = filtered_value
        else:
            filtered_dict[key] = value
    return filtered_dict


def main():
    parser = argparse.ArgumentParser(
        description='Filter diff based on baseline.')
    parser.add_argument('base_line_diff_file',
                        type=str,
                        help='Path to the base line diff file')
    parser.add_argument('diff_file', type=str, help='Path to the diff file')
    parser.add_argument('filtered_out',
                        type=str,
                        help='Path to the output filtered diff file')
    args = parser.parse_args()

    # Generate the filter list
    filter_list = generate_filter_list(args.base_line_diff_file)

    # Specify strings to filter out if the key contains any of them
    filter_strings = []

    # Specify versions and corresponding errors to filter out
    version_error_map = {}

    # Load the new diff
    with open(args.diff_file) as f:
        diff = json.load(f)

    # Filter the diff
    filtered_diff = filter(diff, filter_list)

    # Print or do something with the filtered diff
    with open(args.filtered_out, 'w') as f:
        json.dump(filtered_diff, f, indent=4)


if __name__ == '__main__':
    main()
