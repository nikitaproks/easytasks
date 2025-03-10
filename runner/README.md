## Security implications solutions:
### DoS and Resource Exhaustion
- [ ] Implement rate limiting
- [ ] Implement timeout for script execution `timeout 30s python script.py`
- [ ] Set CPU & Memory limits using Docker's --memory, --cpu-quota

### Arbitrary Code Execution (RCE) & Sandbox Escapes
- [ ] Restricted user for runner
- [ ] Use gVisor or Firecracker for syscall filtering
- [ ] Disable networking inside the container (--network=none)
- [ ] Docker isolation (--network=none, --memory=256m, --cpu-quota=50000).
- [ ] Seccomp syscall restrictions (disable execve, fork, etc.).
- [ ] Python module blocking (disable import os & subprocess).
- [ ] AST code scanning (reject scripts before running).


### Unsafe Package Usage
- [ ] Limit available packages (use pip install --no-index to prevent fetching arbitrary PyPI packages).
- [ ] Use a package allowlist (e.g., only allow numpy, pandas).
- [ ] Scan dependencies with pip-audit or safety


### Command Injection & SSRF Risks
- [ ] Run containers with --read-only mode
- [ ] Block Local IP Ranges (SSRF Protection)
- [ ] Intercept dangerous function calls using AST parsing or runtime analysis.

### Malicious Scheduling Attacks
- [ ] Rate-limit job submissions per user
- [ ] Enforce per-user quotas (e.g., max 5 running jobs).
- [ ] Require prepaid credits to prevent abuse.


### Networking Restrictions in Docker
- [ ] Add whitelist for outgoing requests
- [ ] Rate limiting for outgoing requests
