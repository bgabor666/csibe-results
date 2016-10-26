#!/usr/bin/python

import os
import subprocess

relative_file_paths = []

for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        relative_path = os.path.join(root, name)
        if relative_path[2:].startswith('clang-trunk'):
            relative_file_paths.append(relative_path)

json_root = 'daily-results'

loop_counter = 0

for file_path in relative_file_paths:
    result_basename = os.path.basename(file_path)
    result_dirname = os.path.dirname(file_path)
    result_date = result_basename[:10]
    #if result_basename.startswith('2016-10-01'):
        #print result_dirname
        #print '\t{}'.format(result_date)
        #print '\t{}'.format(result_basename)

    json_result_dir = os.path.join(json_root, result_date.replace('-', '/')[:-3])
    if not os.path.isdir(json_result_dir):
        os.makedirs(json_result_dir)
    json_result_file_path = os.path.join(json_result_dir, '{}-results.json'.format(result_date))
    subprocess.call(['python', 'bin/csibe_csv_to_json.py', '--csv-path', os.path.abspath(file_path), '--json-path', os.path.abspath(json_result_file_path)])
    print file_path
    print json_result_dir
    print json_result_file_path
    loop_counter += 1
    print 'loop_counter: {}'.format(loop_counter)

        #with open(os.path.join('daily-results/2016/10', '2016-10-01.txt'), 'a') as aggregate_file:
        #    aggregate_file.write('{}\n'.format(result_basename))

