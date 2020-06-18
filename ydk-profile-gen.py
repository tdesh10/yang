#!/usr/local/bin/python3
import argparse
import json
import sys
import fnmatch
import os
from sh import ls
from git import Repo

parser = argparse.ArgumentParser()

parser.add_argument("path")
parser.add_argument('--os-name', required=True, choices=['Cisco-IOS-XR', 'Cisco-IOS-XE', 'Cisco-NX-OS'])
parser.add_argument('--version', required=True)
parser.add_argument('--core-version', required=True)
parser.add_argument('--dependency-name', required=True)
parser.add_argument('--dependency-version', required=True)
parser.add_argument('--dependency-core-version', required=True)
parser.add_argument('--dependency-uri', required=True)

args = parser.parse_args()

profile_path = args.path

if profile_path[-1] is '/':
    profile_path = profile_path[:-1]

os_name = args.os_name

version = args.version

core_version = args.core_version

dependency_name = args.dependency_name

dependency_version = args.dependency_version

dependency_core_version = args.dependency_core_version

dependency_uri = args.dependency_uri

repo = Repo(os.getcwd())

remote_repo_url = repo.remotes.origin.url


commit_id = repo.commit('HEAD').hexsha
dir_files = ls(profile_path).split()

os_files = []
tailf_files = []
other_files = []

dir_files.sort()
for dir_file in dir_files:
    if (fnmatch.fnmatch(dir_file, '*deviations.yang')) or ('openconfig' in dir_file) or ('ietf' in dir_file) or ('iana' in dir_file):
        continue
    elif fnmatch.fnmatch(dir_file, f'{os_name}*.yang'):
        os_files.append(profile_path + '/' + dir_file)
    elif fnmatch.fnmatch(dir_file, 'tailf*.yang'):
        tailf_files.append(profile_path + '/' + dir_file)
    elif fnmatch.fnmatch(dir_file, '*.yang'):
        other_files.append(profile_path + '/' + dir_file)


# converst list to a string without [] but keeps elementes with quotes and
# separated with ",\n"
def convert_to_json_file_list(file_list):
    if file_list:
        return (',\n                ').join('\"{0}\"'.format(elem) for elem in file_list)
    else:
        return ''

os_files = convert_to_json_file_list(os_files)
if os_files and (tailf_files or other_files):
    os_files += ',' + '\n\n                '

tailf_files = convert_to_json_file_list(tailf_files)
if tailf_files and other_files:
    tailf_files += ',' + '\n\n                '


other_files = convert_to_json_file_list(other_files)

yang_files = os_files + tailf_files + other_files

template_vars = {
    'version': version,
    'core_version': core_version,
    'url': remote_repo_url,
    'commit_id': commit_id,
    'yang_files': yang_files,
    'dependency_name': dependency_name,
    'dependency_version': dependency_version,
    'dependency_core_version': dependency_core_version,
    'dependency_uri': dependency_uri
}

with open(f'{os_name}_template.json', 'r') as template:
    template_string = template.read()
    print(template_string.format(**template_vars))
