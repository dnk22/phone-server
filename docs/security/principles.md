# Security principles

- Never expose the Device Agent directly to an untrusted network.
- Do not accept arbitrary shell commands as an agent protocol.
- Keep credentials out of Git and generated artifacts.
- Treat FastAPI as the future policy and authentication boundary.
- Validate all cross-process messages against versioned contracts.
- Use least privilege for Android, Termux, CI, and deployment credentials.

The foundation contains no ADB command execution, raw remote shell, frontend auth, or production deployment.
