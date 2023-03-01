terraform {
  required_providers {
    proxmox = {
      source  = "telmate/proxmox"
      version = "2.9.11"
    }
  }
}

resource "proxmox_vm_qemu" "ubuntu-vm" {
  name                   = "ubuntu-${var.type}-${var.node}"
  target_node            = "pve${var.node}"
  onboot                 = true
  oncreate               = true
  clone                  = "ubuntu-jammy-template"
  full_clone             = true
  define_connection_info = false
  agent                  = 1
  os_type                = "cloud-init"
  cores                  = 4
  cpu                    = "host"
  memory                 = 8192
  bootdisk               = "scsi0"
  disk {
    slot     = 0
    size     = "100G"
    type     = "scsi"
    storage  = "local-zfs"
    iothread = 1
  }
  network {
    model  = "virtio"
    bridge = "vmbr0"
  }
  ipconfig0 = "ip=${var.ip}/24,gw=192.168.85.1"
}
