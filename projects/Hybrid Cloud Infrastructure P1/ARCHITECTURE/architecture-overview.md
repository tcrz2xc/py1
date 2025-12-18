# Architecture Overview

RemoteVault is a hybrid home-lab + cloud architecture designed for:

- Secure external access
- Minimal exposed ports
- Container isolation
- Expandability into AI and private search

### Traffic Flow
Internet → Cloudflare Edge → Tunnel → Local Containers → NAS Storage

### Security Layers
- Cloudflare Zero Trust
- No inbound port forwarding
- Tailscale for admin access only
- DNS filtering via AdGuard
