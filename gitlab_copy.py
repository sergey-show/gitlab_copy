#!/usr/bin/env python3

import requests
import json
import git
import os
import yaml

def CopyProjects(url,groups):
    for group in groups:
        gitlab="https://%s/api/v4/groups/%s/projects"% (url, group)
        try:
            projects=requests.get("%s"%gitlab)
        except requests.exceptions.HTTPError:
            print("HTTP Error")
            exit(1)
        if projects.ok:
            if not os.path.exists(group.upper()):
                os.makedirs(group.upper())
            projects=json.loads(projects.text)
            for link in projects:
                print("Copy: " + link["name_with_namespace"])
                try:
                    g = git.cmd.Git(group.upper())
                    g.clone(link["http_url_to_repo"])
                except Exception as e:
                    print(e)
        else:
            print(projects.text)
    return True

def main():
    with open('config.yaml', 'r') as yml_file:
        cfg = yaml.load(yml_file, yaml.FullLoader)
    return CopyProjects(cfg['url'],cfg['groups'])

if __name__ == '__main__':
    main()
