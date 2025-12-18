# Jellyfin — Troubleshooting & Best Practices

## Symptoms: Libraries not populating
- Root causes: permissions, wrong mount path, incomplete scan, incorrect library type

## Fix checklist
1. Confirm container mount paths match actual host paths.
2. Set container PUID/PGID to match file owner (often 1000).
3. Adjust permissions: sudo chown -R 1000:1000 /path/to/media
4. In Jellyfin UI: Manage Libraries -> Force Full Scan
5. Clear metadata if stale and rescan

## Performance tips
- Enable hardware acceleration if available
- Use separate directories for metadata/cache mounted to host