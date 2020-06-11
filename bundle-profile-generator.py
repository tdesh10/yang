#!/usr/local/bin/python3
import json
import sys
import fnmatch
from sh import git, ls

profile_path = sys.argv[1]

version = profile_path.split('/')[-1]

remote_repo_url = git.remote('-v').split()[1]

commit_id = str(git('rev-parse', 'HEAD')).strip()

yang_files = fnmatch.filter(ls(profile_path).split(), '*.yang')

yang_files = [profile_path + '/' + filename for filename in yang_files]

bundle_profile = {
    "name": "cisco-ios-xr",
    "version": version,
    "core_version": "0.6.0",
    "author": "Cisco",
    "copyright": "Cisco",
    "description": "YDK bundle for Cisco IOS XR models",
    "long_description": "This YANG Development Kit (YDK) bundle provides APIs for Cisco IOS XR YANG models. YDK facilitates the use of YANG data models by expressing the model semantics in an API and abstracting protocol/encoding details.  YDK is composed of a core package that defines services and providers, plus one or more module bundles.  This YDK bundle for Cisco IOS XR models uses the YDK core package and additional model bundles.  You can find the SDK documentation at http://ydk.cisco.com/py/docs",
    "git" : {
        "url": remote_repo_url,
        "commitid": commit_id,
        "files" : yang_files
    }
}

print(json.dumps(bundle_profile, indent=4, separators=(",", ":")))
