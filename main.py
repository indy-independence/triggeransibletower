#!/usr/bin/env python2

import requests
import pprint

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

import settings

def tower_authenticate(username=settings.tower_username, password=settings.tower_password):
    url = '{}/api/v2/authtoken/'.format(
        settings.tower_api_url
    )
    headers = { 'Content-Type': 'application/json' }
    data = {
        'username': username,
        'password': password,
    }
    r = requests.post(url, headers=headers, json=data, verify=settings.tower_verify_ssl)
    if r.status_code == 200:
        return r.json()
    else:
        print r.status_code
        print r.text
        raise Exception

def launch_job(jobid, token, extra_vars=None):
    url = '{}/api/v2/job_templates/{}/launch/'.format(
        settings.tower_api_url,
        jobid
    )
    headers = {
        'Content-Type': 'application/json',
        'Authorization':  'Token {}'.format(token['token']),
    }
    if extra_vars:
        data = {
            'extra_vars': extra_vars
        }
    else:
        data = None
    r = requests.post(url, headers=headers, json=data, verify=settings.tower_verify_ssl)
    if r.status_code == 201:
        pprint.pprint(r.json())
    else:
        print r.status_code
        print r.text
        raise Exception

if __name__ == "__main__":
    token = tower_authenticate()
    launch_job(7, token, extra_vars={
        'interface': 'GigabitEthernet0/0/0/1',
        'description': 'ansibletowertest',
        'ipaddress': '172.16.0.1 255.255.255.0',
    })
    print "Press any key to deconfigure interface again"
    raw_input()
    launch_job(10, token, extra_vars={
        'interface': 'GigabitEthernet0/0/0/1',
    })

