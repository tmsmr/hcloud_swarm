#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from python_terraform import Terraform
import json
import re
import os

ANSIBLE_SSH_PORT = '2222'

def main():
    t = Terraform()
    state = json.dumps(t.tfstate.modules)
    ips = set(re.findall(r'[0-9]+(?:\.[0-9]+){3}', state))
    for ip in ips:
        os.system('ssh-keygen -R %s' % ip)
        os.system('ssh-keyscan -H %s >> ~/.ssh/known_hosts' % ip)
        os.system('ssh-keyscan -H -p %s %s >> ~/.ssh/known_hosts' % (ANSIBLE_SSH_PORT, ip))

if __name__ == "__main__":
    main()
