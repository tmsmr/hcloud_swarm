output "swarm-primary-managers" {
  value = "${map(
    hcloud_server.swarm-primary-manager.name, hcloud_server.swarm-primary-manager.ipv4_address
  )}"
}

output "swarm-secondary-managers" {
  value = "${zipmap(
    hcloud_server.swarm-secondary-manager.*.name, hcloud_server.swarm-secondary-manager.*.ipv4_address
  )}"
}

output "swarm-workers" {
  value = "${zipmap(
    hcloud_server.swarm-worker.*.name, hcloud_server.swarm-worker.*.ipv4_address
  )}"
}

output "ssh-public-key" {
  value = "${data.hcloud_ssh_key.deploy.public_key}"
}
