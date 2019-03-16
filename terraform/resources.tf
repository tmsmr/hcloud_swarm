provider "hcloud" {
  token = "${var.hcloud_token}"
}

resource "hcloud_server" "swarm-primary-manager" {
  name        = "swarm-primary-manager"
  image       = "${var.os-image}"
  server_type = "${var.swarm-manager-type}"
  datacenter  = "${data.hcloud_datacenter.nuremberg.name}"
  ssh_keys    = ["${data.hcloud_ssh_key.deploy.id}"]
}

resource "hcloud_server" "swarm-secondary-manager" {
  name        = "swarm-secondary-manager-${count.index}"
  image       = "${var.os-image}"
  server_type = "${var.swarm-manager-type}"
  datacenter  = "${data.hcloud_datacenter.nuremberg.name}"
  ssh_keys    = ["${data.hcloud_ssh_key.deploy.id}"]
  count       = "${var.count-swarm-secondary-managers}"
}

resource "hcloud_server" "swarm-worker" {
  name        = "swarm-worker-${count.index}"
  image       = "${var.os-image}"
  server_type = "${var.swarm-worker-type}"
  datacenter  = "${data.hcloud_datacenter.nuremberg.name}"
  ssh_keys    = ["${data.hcloud_ssh_key.deploy.id}"]
  count       = "${var.count-swarm-workers}"
}
