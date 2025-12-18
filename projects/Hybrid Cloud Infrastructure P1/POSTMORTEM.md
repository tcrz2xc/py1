---

# **POSTMORTEM.md**  

```markdown
# RemoteVault Cloud & Media Stack Postmortem

## Project Summary

The RemoteVault project aimed to integrate a comprehensive full-stack environment that included cloud servers, NAS integration, media servers, VPN connectivity, DNS management, and VM testing. The goal was to provide seamless external access without the need for VPN on every device, while also maintaining robust local network functionality.

---

## **Challenges Encountered**

1. **Cloudflare Tunnel Ingress Rules Overwriting**
   - Multiple attempts with duplicate hostnames initially caused rules to be ignored.
   - Default published routes were overriding the intended configuration.
   - Required upgrading cloudflared version from 16 → 19 to fully support custom path-based rules.

2. **Jellyfin Base URL Edge Case**
   - Setting a Base URL caused repeated redirect loops and 404 errors.
   - Removing the Base URL and mapping the container port directly solved the issue.

3. **Container Networking**
   - Jellyfin and Cloudflare were in separate containers; bridge network required careful IP mapping.
   - Curling the local IP initially returned no data due to bridge isolation; mapping the correct host ports resolved the connectivity.

4. **Tailscale VPN Considerations**
   - While useful for administrative access, Tailscale required awareness of internal routing to avoid conflicts with Cloudflare Tunnel.

---

## **Lessons Learned**

- Always verify container-to-container connectivity when using bridge networks.
- Keep ingress rules explicit and unique; duplicate hostnames can silently break routing.
- Upgrading cloudflared can solve subtle edge cases with routing and path matching.
- Document each technical step, especially for complex tunnel setups; this is invaluable for replication or sharing with recruiters.

---

## **Key Wins**

- Successful deployment of Jellyfin accessible externally at `https://jellyfin.remotevault.cc`.
- Full integration of cloud server, NAS, VPN, and media servers into a cohesive environment.
- Creation of modular folders for VMs (Kali, Windows, Proxmox) for future expansion.
- Recruiter-friendly narrative: demonstrated real-world DevOps, infrastructure, and full-stack integration skills.

---

## **Future Improvements**

- Add automated TLS/SSL provisioning for all services.
- Expand VM testing with Windows and additional Linux distros.
- Implement performance monitoring and metrics aggregation across the full stack.
