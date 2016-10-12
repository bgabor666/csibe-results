#!/usr/bin/env python

import argparse
import json
import os


def copy_csibe_results_from_csv_to_json(csv_path, json_path):
    with open(csv_path) as csv_file:
        csv_contents = csv_file.read().splitlines()

    csv_path_basename = os.path.basename(csv_path)
    target_name = csv_path_basename[11:-20]

    llvm_revision = csv_contents[4].split(',')[1]
    build_date = csv_path_basename[:10]

    result_dict = {}
    result_list = [element.split(',') for element in csv_contents[6:]]
    for split_result in result_list:
        project_name = split_result[0]
        project_result = int(split_result[2])
        if project_name not in result_dict:
            result_dict[project_name] = 0
        result_dict[project_name] += project_result

    result_sum = sum(result_dict.values())

    if not os.path.isfile(json_path):
        json_data = {'revisions': {}, 'date': build_date}
    else:
        with open(json_path) as json_file:
            json_data = json.load(json_file)
    
    if llvm_revision not in json_data['revisions']:
        json_data['revisions'][llvm_revision] = {}

    target_flags = csv_contents[1].split(',')[1].split()
    target_details = {'flags': target_flags, 'projects': result_dict, 'sum': sum(result_dict.values())}
    json_data['revisions'][llvm_revision][target_name] = target_details

    print json.dumps(json_data, sort_keys=True, indent=4, separators=(',',':'))

    with open(json_path, 'w') as json_file:
        json.dump(json_data, json_file, sort_keys=True, indent=4, separators=(',',':'))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv-path")
    parser.add_argument("--json-path")

    args = parser.parse_args()

    copy_csibe_results_from_csv_to_json(args.csv_path, "test.json")
