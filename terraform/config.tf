variable "os-image" {
  default = "centos-7"
}

variable "swarm-manager-type" {
  default = "cx11"
}

variable "count-swarm-secondary-managers" {
  default = 2
}

variable "swarm-worker-type" {
  default = "cx31"
}

variable "count-swarm-workers" {
  default = 3
}

variable "hcloud_token" {}

data "hcloud_datacenter" "nuremberg" {
  name = "nbg1-dc3"
}

data "hcloud_ssh_key" "deploy" {
  name = "deploy"
}
