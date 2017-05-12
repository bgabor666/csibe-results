#!/usr/bin/env python

import argparse
import json
import os

machine_name_base = "LNT-CSiBE-"

default_start_time = "01:00:00"
default_end_time = "01:01:00"

lnt_test_data_template = {
                           "Data": [
                           ],
                           "Info": {},
                           "Name": ""
                         }

lnt_json_template = {
                      "Machine": {
                        "Info": {
                        },
                        "Name": ""
                      },
                      "Run": {
                        "End Time": "",
                        "Start Time": "",
                        "Info": {
                          "run_order": "",
                          "tag": "nts"
                        } 
                      },
                      "Tests": [
                      ]
                    }

def copy_csibe_results_from_csv_to_json(csv_path, json_path):
    with open(csv_path) as csv_file:
        csv_contents = csv_file.read().splitlines()

    csv_path_basename = os.path.basename(csv_path)
    target_name = csv_path_basename[11:-20]

    llvm_revision = csv_contents[4].split(',')[1]
    build_date = csv_path_basename[:10]

    json_data = lnt_json_template
    json_data["Machine"]["Name"] = machine_name_base + target_name[12:] 
    json_data["Run"]["End Time"] = build_date + " " + default_end_time
    json_data["Run"]["Start Time"] = build_date + " " + default_start_time
    json_data["Run"]["Info"]["run_order"] = llvm_revision

    test_result_list = []
    result_list = [element.split(',') for element in csv_contents[6:]]
    for split_result in result_list:
        project_name = split_result[0]
        object_name = split_result[1]
        object_result = int(split_result[2])
        test_result_list.append({"Data": [object_result], "Info": {}, "Name": "nts." + project_name + "/" + object_name + ".code_size"})

    json_data["Tests"] = test_result_list

    print json.dumps(json_data, sort_keys=True, indent=4, separators=(',',':'))

    with open(json_path, 'w') as json_file:
        json.dump(json_data, json_file, sort_keys=True, indent=4, separators=(',',':'))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv-path")
    parser.add_argument("--json-path")

    args = parser.parse_args()

    copy_csibe_results_from_csv_to_json(args.csv_path, args.json_path)
