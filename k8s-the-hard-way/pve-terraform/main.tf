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

resource "proxmox_vm_qemu" "test_server" {
  count       = 1
  name        = "test-vm-${count.index + 1}"
  target_node = "pve1"
  clone       = "ubuntujammytemplate"
  agent       = 1
  os_type     = "cloud-init"
  cores       = 3
  cpu         = "host"
  memory      = 4096
  bootdisk    = "scsi0"
  disk {
    slot = 0
    # set disk size here. leave it small for testing because expanding the disk takes time.
    size     = "10G"
    type     = "scsi"
    storage  = "local-zfs"
    iothread = 1
  }
  network {
    model  = "virtio"
    bridge = "vmbr0"
  }
  ipconfig0 = "ip=192.168.85.9${count.index + 1}/24,gw=192.168.85.1"
}
