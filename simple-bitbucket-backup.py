#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import json
import base64
import shutil
import datetime
import os
import errno

bbuser = "username"
bbpass = "password"
storage = "/home/user/bitbucket-archive/"

now = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")

credentials = base64.b64encode("{0}:{1}".format(
    bbuser, bbpass).encode()).decode("ascii")
headers = {'Authorization': "Basic " + credentials}

def req(url):
   request = urllib.request.Request(
      url=url, headers=headers)
   response = urllib.request.urlopen(request)
   response_data = json.loads(response.read())
   response.close()
   return response_data

def download(url, save_path, name):
   if not os.path.exists(os.path.dirname(save_path + name)):
      try:
         os.makedirs(os.path.dirname(save_path + name))
      except OSError as exc:
         if exc.errno != errno.EEXIST:
            raise
   try:
      request = urllib.request.Request(
          url=url, headers=headers)
      resp = urllib.request.urlopen(request)
      with resp as response, open(save_path + name, 'wb') as out_file:
         shutil.copyfileobj(response, out_file)
   except urllib.error.HTTPError as err:
      if err.code == 404:
         print('404 on: ' + url)
      else:
         raise


def get_repo_list():
   resp = req('https://bitbucket.org/api/2.0/repositories/?role=member')
   repo_list = {}
   for repo in resp['values']:
      repo_list[repo['name']] = repo['full_name']


   while resp.get('next'):
      resp = req(resp['next'])
      for repo in resp['values']:
         repo_list[repo['name']]=repo['full_name']
      return repo_list
       
def get_all_downloads():
   repo_list = get_repo_list()
   '''
   Repository list to backup in dict
   {'MyLovelyRepo': 'username/mylovelyrepo', 'MyWorkRepo': 'google/userdatacollector'}
   '''
   download_list = {}
   for full_name in repo_list.values():
      branches = []
      resp = req('https://bitbucket.org/api/2.0/repositories/%s/refs/branches' % full_name)
      for branch in resp['values']:
         branches.append(branch['name'])
      download_list[full_name] = branches
   return download_list


def do_backup():
   download_list = get_all_downloads()
   backup_path = storage + now + '/'

   for full_name, branch in download_list.items():
      for branch in branch:
         print(full_name + ':' + branch)
         download(
            'https://bitbucket.org/%s/get/%s.zip' % (full_name, branch),
            backup_path + full_name + '/',
            branch + '-' + now + '.zip'
            )
   

do_backup()
