#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os

ANSIBLE_SSH_PORT = '2222'

def get_args():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--flatlist', action='store_true')
    parser.add_argument('--list', action='store_true')
    parser.add_argument('--host')
    parser.add_argument('--accept', action='store_true')
    return parser.parse_args()

def wd_to_script_dir():
    import os
    path = os.path.abspath(__file__)
    dir = os.path.dirname(path)
    os.chdir(dir)

def terraform_output(key):
    ret = os.popen('terraform output -json ' + key).read()
    return json.loads(ret)

def main():
    args = get_args()
    wd_to_script_dir()
    primary_managers = terraform_output('swarm-primary-managers')
    secondary_managers = terraform_output('swarm-secondary-managers')
    workers = terraform_output('swarm-workers')
    ssh_public_key = terraform_output('ssh-public-key')
    if args.flatlist:
        hosts = list(primary_managers.keys())
        hosts.extend(list(secondary_managers.keys()))
        hosts.extend(list(workers.keys()))
        print('\n'.join(hosts))
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
    if args.accept:
        hosts = {**primary_managers, **secondary_managers, **workers}
        for host in hosts:
            ip = hosts[host]
            os.system('ssh-keygen -R %s' % ip)
            os.system('ssh-keyscan -H %s >> ~/.ssh/known_hosts' % ip)
            os.system('ssh-keyscan -H -p %s %s >> ~/.ssh/known_hosts' % (ANSIBLE_SSH_PORT, ip))

if __name__ == "__main__":
    main()
