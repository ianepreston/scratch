terraform {
  required_providers {
    proxmox = {
      source  = "telmate/proxmox"
      version = "2.9.11"
    }
  }
}
provider "proxmox" {
  pm_tls_insecure = true
  pm_api_url      = "https://pve1.local.ipreston.net:8006/api2/json"
}

locals {
  nodetypes = {
    "controller" = 0
    "worker"     = 3
  }
  vm_attrs_list = flatten([
    for nodetype, baseoctet in local.nodetypes : [
      for i in range(3) : {
        name = "${nodetype}${i}"
        node = "${i + 1}",
        type = "${nodetype}",
        ip   = "192.168.85.${70 + baseoctet + i}"
      }
    ]
  ])
  vm_attrs_map = {
    for obj in local.vm_attrs_list : "${obj.name}" => obj
  }

}

module "ubuntu_vm" {
  source   = "./modules/ubuntu-vm"
  for_each = local.vm_attrs_map
  node     = each.value.node
  type     = each.value.type
  ip       = each.value.ip
}
