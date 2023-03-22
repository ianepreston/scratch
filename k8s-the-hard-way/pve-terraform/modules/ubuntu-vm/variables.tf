variable "node" {
  description = "Proxmox node number to deploy to"
  type        = number
}

variable "type" {
  description = "A controller or worker node"
  type        = string
}

variable "ip" {
  description = "The static IP for the VM"
  type        = string
}
