#!/usr/bin/python

import os

relative_file_paths = []
relative_dir_paths = []

for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        relative_path = os.path.join(root, name)
        if relative_path[2:].startswith('clang-trunk'):
            relative_file_paths.append(relative_path)

for file_path in relative_file_paths:
    result_basename = os.path.basename(file_path)
    result_dirname = os.path.dirname(file_path)
    result_date = result_basename[:10]
    if result_basename.startswith('2016-10-01'):
        print result_dirname
        print '\t{}'.format(result_date)
        print '\t{}'.format(result_basename)

        with open(os.path.join('daily-results/2016/10', '2016-10-01.txt'), 'a') as aggregate_file:
            aggregate_file.write('{}\n'.format(result_basename))

