# NAS (UGREEN) — Full Guide

## Overview
UGREEN NAS runs Docker; host Jellyfin, AdGuard, Tailscale, Plex, and plan for VMs.

## Docker best practices
- Use named volumes on a dedicated disk.
- Ensure correct UID/GID for media access (often 1000:1000).
- Backup config dirs regularly.

## AdGuard
- Host at <server-ip>:54
- If router intercepts DNS, set DNS per-device to the NAS.
- Use query log to verify clients.

## Tailscale
- Use Tailscale for remote access; see docs/tailscale.md for full steps.
