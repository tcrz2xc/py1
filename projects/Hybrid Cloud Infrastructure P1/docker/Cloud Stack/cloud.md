# Cloud Server (Oracle) — Full Guide

## Overview
This guide explains how to provision and operate the cloud server that hosts Nextcloud and related services:
Nginx Proxy Manager, MariaDB, Redis, OnlyOffice.

## Prerequisites
- Oracle Cloud VM with public IP
- SSH access, sudo
- Domain (DuckDNS or similar)
- Open ports 80/443 in OCI security lists and host firewall

## Steps
1. Update OS.
2. Install Docker & Docker Compose plugin.
3. Prepare directories and .env with secrets.
4. Deploy with docker compose.
5. Configure Nginx Proxy Manager to secure Nextcloud and OnlyOffice.
6. Update Nextcloud config.php to force HTTPS and trusted proxies.
7. Set up backups (mysqldump + rclone sync to NAS).

## Notes
- Use Watchtower cautiously for auto-updates.
- For Nextcloud occ commands, run as www-data inside container.