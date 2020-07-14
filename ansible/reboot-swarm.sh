#!/usr/bin/env bash

set -xe

hosts=`../terraform/terraform-swarm-inventory.py --flatlist`
for host in $hosts; do
	ansible-playbook -i ../terraform/terraform-swarm-inventory.py -e target=$host swarm-host-reboot.yml
done
