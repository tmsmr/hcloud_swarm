#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from python_terraform import Terraform
import json

ANSIBLE_SSH_PORT = '2222'

def get_args():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--list', action='store_true')
    parser.add_argument('--host')
    return parser.parse_args()

def wd_to_script_dir():
    import os
    path = os.path.abspath(__file__)
    dir = os.path.dirname(path)
    os.chdir(dir)

def main():
    args = get_args()
    wd_to_script_dir()
    t = Terraform()
    primary_managers = t.output('swarm-primary-managers')
    secondary_managers = t.output('swarm-secondary-managers')
    workers = t.output('swarm-workers')
    ssh_public_key = t.output('ssh-public-key')
    if args.list:
        inventory = {
            'swarm-primary-managers': list(primary_managers.keys()),
            'swarm-secondary-managers': list(secondary_managers.keys()),
            'swarm-workers': list(workers.keys())
        }
        print(json.dumps(inventory))
    if args.host:
        hosts = {**primary_managers, **secondary_managers, **workers}
        print(json.dumps({
            'ansible_host': hosts[args.host],
            'ansible_port': ANSIBLE_SSH_PORT,
            'ssh_public_key': ssh_public_key
        }))

if __name__ == "__main__":
    main()
