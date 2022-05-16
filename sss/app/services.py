import os, sys
import re
import requests
import base64
import json
from tempfile import TemporaryFile
from configparser import RawConfigParser
from .settings import LocalSettings
from github import Github

requests.packages.urllib3.disable_warnings()

class MyGithub(Github):
    
    # base_url=github_api_url, login_or_token=git_token, verify=False
    def __init__(self, *args, **kvargs):
        self.API_URL = LocalSettings.GIT_API_URL
        self.GIT_TOKEN = LocalSettings.GIT_TOKEN
        self.REQUEST_VERIFY = LocalSettings.GIT_REQUESTS_VERIFY
        if "git_api_url" in kvargs:
            self.API_URL = kvargs["git_api_url"]
        if "token" in kvargs:
            self.GIT_TOKEN = kvargs["token"]
        if "verify" in kvargs:
            self.REQUEST_VERIFY = kvargs["verify"]

        Github.__init__(    self, 
                            base_url=self.API_URL, 
                            login_or_token=self.GIT_TOKEN, 
                            verify=self.REQUEST_VERIFY)

    #
    # Get sha of file at path_name
    #
    def get_blob_sha(self, repo_object, path_name, branch="production"):
        # first get the branch reference
        ref = repo_object.get_git_ref(f'heads/{branch}')
        # then get the tree
        tree = repo_object.get_git_tree(ref.object.sha, recursive='/' in path_name).tree
        # look for path in tree
        sha = [x.sha for x in tree if x.path == path_name]
        if not sha:
            return None
        return sha[0]

    #
    # PyGithub has a get_content however it does not work with large files
    #
    def get_blob_content(self, repo_object, path_name, branch="production"):
        sha = self.get_blob_sha(repo_object, path_name, branch)
        if not sha:
            return None
        # we have sha
        blob = repo_object.get_git_blob(sha)
        base64_content = blob.content
        content_string = base64.b64decode(base64_content)
        contents = content_string.decode('utf-8')
        return sha, contents

    #
    # get conf file from git and convert to dict
    #
    def get_conf_file(self, repo_name, file_path, branch="production"):
        repo = self.get_repo(repo_name)
        print(repo_name, repo, file_path, branch)
        sha, content = self.get_blob_content(repo, file_path, branch)
        parser = RawConfigParser(strict=False)
        with TemporaryFile(mode='w+t') as f:
            f.write(content)
            f.seek(0)
            parser.readfp(f)
        the_dict = {}
        for section in parser.sections():
            the_dict[section] = {}
            for key, val in parser.items(section):
                the_dict[section][key] = val

        return sha, the_dict

    # Use search_repo to find server_name in whitelist repo
    def grep_repo(self, search_string, repo_name):
        query = "q=%s in:file repo:%s" % (search_string, repo_name)
        results = self.search_code(query)
        return [x.name for x in results]
