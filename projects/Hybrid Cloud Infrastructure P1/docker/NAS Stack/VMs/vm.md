# VM Subsystem Planning — Getting a Remote Workstation

## Goals
- Run GUI workstation VM accessible remotely via Tailscale.
- Use VMs for testing server images and configs.
- Isolate experimental services from production containers.

## Options & Steps
- If NAS supports KVM: install libvirt/qemu and create VMs via virt-manager or NAS UI.
- Else: consider a small Proxmox or dedicated machine for VMs.
- Each VM should run Tailscale for seamless mesh access.