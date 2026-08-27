# Security

## Reporting

Email `security@playnexus.io` — do not open public issues for vulnerabilities.

## Model

- Capabilities: READ_FILES, WRITE_FILES, DELETE_FILES, EXECUTE_COMMANDS, NETWORK_ACCESS, BROWSER_ACCESS, SYSTEM_CONTROL, INSTALL_SOFTWARE, ACCESS_SECRETS
- Enforcement: PermissionManager → Policy (allow/deny/ask) → Risk → Sandbox (Host / Host+checkpoint / Docker) → AuditLog
- Secrets: OS keychain only, never in prompts/logs
- Checkpoints before destructive ops; rollback on verify fail
- Audit log append-only at `audit_logs` table

## Hardening checklist

- [ ] HIGH tools sandboxed in Docker by default
- [ ] Network disabled unless task needs it
- [ ] User can delete any memory with one click (Memory UI)
