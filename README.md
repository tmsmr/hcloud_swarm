# Swarm Cluster on Hetzner Cloud

This collection of Terraform configs, Ansible playbooks and some other utilities helps to deploy and maintain a Docker Swarm Cluster + some basic tools (biased) on Hetzner Cloud instances.

Everything here works semi-automatic. The goal is to make maintenance easier, don't expect to get a magically working/self-managing cluster: You still need to know the tools and understand whats happening! If you brick something, destroy your backups or something like that, don't blame me.

## Create instances with Terraform (in dir terraform)
- Create project in Hetzner Cloud
- Add your SSH-key as 'deploy' (that name is referenced later) to the project
- Create an API-key for the project and configure it in 'secrets.auto.tfvars'
- Adjust scaling in 'config.tf'
- Initialize project: `terraform init`
- Apply project: `terraform apply`
- Store/commit generated 'terraform.tfstate' (Terraform is NOT stateless)
- Install the 'python-terraform' Python module
- (Accept SSH host keys: `./accept-new-host-keys.py`)

## Deploy/Configure instances with Ansible (in dir ansible)
- (Change into 'roles' and install dependencies: `ansible-galaxy install --roles-path . -r requirements.yml`)
- (Configure Docker version in 'vars/docker_vars.yml' (`yum list docker-ce --showduplicates | sort -r`). Be careful: The Docker packaging structure changed after 18.06)
- Configure Hetzner Cloud API-key in 'vars/secret_vars.yml' (Needed for https://github.com/costela/docker-volume-hetzner)
- (Configure the version for 'docker-volume-hetzner' in 'vars/docker_vars.yml')
- Configure SSH to use an alterantive port on the hosts: `ansible-playbook -i ../terraform/terraform-swarm-inventory.py change-sshd-port.yml`. We want Port 22 to be available for more useful stuff...
- Prepare hosts with: `ansible-playbook -i ../terraform/terraform-swarm-inventory.py cluster-maintenance.yml`
- Init swarm with: `ansible-playbook -i ../terraform/terraform-swarm-inventory.py swarm-apply.yml`

## Access Docker remotely (in dir ansible)
- Execute `ansible-playbook -i ../terraform/terraform-swarm-inventory.py docker-socket-access.yml` to prepare remote access.
- Use `utils/docker` as replacement for `docker`. This script forwards the remote `/var/run/docker.sock` to a random tcp port on localhost using SSH, executes the Docker command and terminates the established SSH session afterwards

## DNS Setup
- Create A Records for all Manager nodes: swarm.example.org -> Manager-IP
- Create C-NAME Records: example.org -> swarm.example.org and *.example.org -> swarm.example.org
- Should be done with https://www.terraform.io/docs/providers/dns/index.html if possible

## Deploy basic services
- Change in the 'stacks/basic' folder
- Adjust configuration in 'traefik.toml' and 'basic.yml'
- Execute `../../utils/docker stack deploy -c basic.yml basic`
- Open Portainer and finish the setup

## Useful stuff

### System upgrades
- Run `ansible-playbook -i ../terraform/terraform-swarm-inventory.py cluster-maintenance.yml`
- The nodes are NOT rebooting after the upgrade. You should use `docker-upgrade.yml` for that (explained below)

### Add node to swarm
- Add node to Terraform config
- `terraform apply`
- Run playbooks 'change-sshd-port.yml', 'cluster-maintenance.yml' and 'swarm-apply.yml` again

### Remove node from swarm
- Execute `ansible-playbook -i ../terraform/terraform-swarm-inventory.py -e target=swarm-worker-1 swarm-node-remove.yml`. Replace `target` with node to remove.
- Remove node from Terraform configuration
- `terraform apply`

### Rolling Docker upgrade (Node reboot)
- Upgrade a node using: `ansible-playbook -i ../terraform/terraform-swarm-inventory.py -e target=swarm-worker-1 docker-upgrade.yml`. Replace `target` with node to upgrade.
- The upgrade consists of:
  - Drain the node
  - Upgrade Docker
  - Reboot host
  - Activate the node
- Can also be used to reboot the nodes (e.g. for for activating a new kernel version - just don't change the docker version)

### Various
- Reset swarm: `ansible -i ../terraform/terraform-swarm-inventory.py all -u root -m shell -a "docker swarm leave --force"`
- Execute commands with Ansible: `ansible -i ../terraform/terraform-swarm-inventory.py swarm-primary-manager -u root -m shell -a "systemctl status sshd"`
