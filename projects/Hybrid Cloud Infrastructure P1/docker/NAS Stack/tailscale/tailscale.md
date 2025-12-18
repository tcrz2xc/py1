# Tailscale — Deployment & Best Practices

## Quick deploy (Docker)
1. Create an auth key via https://login.tailscale.com/admin/settings/keys
2. Use the following docker-compose snippet (see docker_compose/nas_stack.yml):
   - mount /var/lib/tailscale for state
   - run tailscaled and accept node in admin
3. Enable MagicDNS for friendly hostnames

## Features to enable
- Tailscale SSH (if desired)
- Exit node on NAS for egress routing (optional)
- Tags for ACLs (e.g., tag:nas, tag:vm)