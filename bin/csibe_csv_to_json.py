#!/usr/bin/env python

import argparse
import json
import os


def copy_csibe_results_from_csv_to_json(csv_path, json_path):
    with open(csv_path) as csv_file:
        csv_contents = csv_file.read().splitlines()

    llvm_revision = csv_contents[4].split(',')[1]
    build_date = os.path.basename(csv_path)[:10]
    print build_date

    if not os.path.isfile(json_path):
        json_data = {'dailyBuilds': {'date': build_date, 'builds': []}}
    else:
        # TODO: Open existing json file and read json_data from there.
        return
    
    json_data['dailyBuilds']['builds'].append({'revision': csv_contents[4].split(',')[1]})

    print csv_contents[1].split(',')[1]
    print csv_contents[4].split(',')[1]
    print json_data
    print json.dumps(json_data, sort_keys=True, indent=4, separators=(',',':'))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv-path")
    parser.add_argument("--json-path")

    args = parser.parse_args()

    copy_csibe_results_from_csv_to_json(args.csv_path, "/dev/null")
