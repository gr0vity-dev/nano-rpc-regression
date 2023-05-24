import argparse
import json
from deepdiff import DeepDiff
import re


class JsonComparator:

    def __init__(self, file1, version1, file2, version2):
        self.file1 = file1
        self.version1 = version1 if version1 else self.get_version(file1)
        self.file2 = file2
        self.version2 = version2 if version2 else self.get_version(file2)

    @staticmethod
    def get_version(filename):
        base_name = filename.split('.')[0]  # Remove file extension
        return base_name.split('_')[-1].replace(
            "-", ".")  # Version is after the last underscore

    @staticmethod
    def nested_set(dic, keys, value):
        for key in keys[:-1]:
            dic = dic.setdefault(key, {})
        dic[keys[-1]] = value

    @staticmethod
    def handle_change(change):
        return str(change.t1 if hasattr(change, 't1') else change.value
                   ), "Item not present"

    @staticmethod
    def handle_add(change):
        return "Item not present", str(
            change.t2 if hasattr(change, 't2') else change.value)

    @staticmethod
    def handle_modify(change):
        return str(change.t1), str(change.t2)

    def separate_keys(self, key_path):
        pattern = r"\['(.+?)'\]\['(.+?)'\]"
        matches = re.search(pattern, key_path)

        part1 = matches.group(1)
        first_key = part1.split("|")[0]
        whole_key = str.join("|", part1.split("|"))
        difference_on_key = matches.group(2)
        return first_key, whole_key, difference_on_key

    def compare(self):
        handlers = {
            "dictionary_item_removed": self.handle_change,
            "iterable_item_removed": self.handle_change,
            "dictionary_item_added": self.handle_add,
            "iterable_item_added": self.handle_add,
            "type_changes": self.handle_modify,
            "values_changed": self.handle_modify,
        }

        with open(self.file1) as f1, open(self.file2) as f2:
            json1 = json.load(f1)
            json2 = json.load(f2)

        diff = DeepDiff(json1, json2, ignore_order=True, view='tree')
        result = {}

        for change_type, changes in diff.items():
            result[change_type] = {}
            if change_type not in handlers:
                print(f"Unhandled change type: {change_type}")
                continue

            for change in changes:
                key_path = str(change.path(root=''))

                # key = self.parse_key(str(change.path(root='')))

                first_key, whole_key, difference_on_key = self.separate_keys(
                    key_path)

                data_format = {
                    'difference_on_key': difference_on_key,
                    self.version1: None,
                    self.version2: None,
                }
                data_format[self.version1], data_format[
                    self.version2] = handlers[change_type](change)

                self.nested_set(result[change_type], [first_key, whole_key],
                                data_format)
        return result


def write_results_to_file(result, filename):
    with open(filename, 'w') as outfile:
        json.dump(result, outfile, indent=4)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Json Comparator script.")
    parser.add_argument("file1", help="First input file.")
    parser.add_argument("version1",
                        nargs='?',
                        default=None,
                        help="Version of the first file.")
    parser.add_argument("file2", help="Second input file.")
    parser.add_argument("version2",
                        nargs='?',
                        default=None,
                        help="Version of the second file.")
    parser.add_argument("-o",
                        "--output",
                        default="deep_diff_result.json",
                        help="Output file.")
    args = parser.parse_args()

    comparator = JsonComparator(args.file1, args.version1, args.file2,
                                args.version2)
    result = comparator.compare()
    write_results_to_file(result, args.output)
