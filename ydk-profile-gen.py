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
parser.add_argument('--version')
parser.add_argument('--core-version')
parser.add_argument('--dependency-name')
parser.add_argument('--dependency-version')
parser.add_argument('--dependency-core-version')
parser.add_argument('--dependency-uri')

args = parser.parse_args()

profile_path = args.path

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

cisco_ios_xr_files = []
tail_f_files = []
other_files = []

for dir_file in dir_files:
    if fnmatch.fnmatch(dir_file, 'Cisco-IOS-XR*.yang'):
        cisco_ios_xr_files.append(profile_path + '/' + dir_file)
    elif fnmatch.fnmatch(dir_file, 'tail_f*.yang'):
        tail_f_files.append(profile_path + '/' + dir_file)
    elif fnmatch.fnmatch(dir_file, '*.yang'):
        other_files.append(profile_path + '/' + dir_file)

with open('cisco-ios-xr_template.json', 'r') as template:
    template_string = template.read()
    print(eval(f'''{}'''.format(template_string)))

# bundle_profile = {
#     "name": "cisco-ios-xr",
#     "version": version,
#     "core_version": "0.6.0",
#     "author": "Cisco",
#     "copyright": "Cisco",
#     "description": "YDK bundle for Cisco IOS XR models",
#     "long_description": "This YANG Development Kit (YDK) bundle provides APIs for Cisco IOS XR YANG models. YDK facilitates the use of YANG data models by expressing the model semantics in an API and abstracting protocol/encoding details.  YDK is composed of a core package that defines services and providers, plus one or more module bundles.  This YDK bundle for Cisco IOS XR models uses the YDK core package and additional model bundles.  You can find the SDK documentation at http://ydk.cisco.com/py/docs",
#     "git" : {
#         "url": remote_repo_url,
#         "commitid": commit_id,
#         "files" : yang_files
#     }
# }

# print(json.dumps(bundle_profile, indent=4, separators=(",", ":")))
