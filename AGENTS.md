# Agent Rules for SecProject

## Project Purpose

This repository is a local, educational Django security lab for a school project. It demonstrates three topics:

1. HTTP compared with HTTPS.
2. SQL injection and its prevention.
3. Session-token security and protective cookie settings.

Do not add unrelated vulnerabilities or features without the user's approval.

## Safety and Scope

- Run and test the application only on localhost or another explicitly approved isolated environment.
- Do not expose an intentionally vulnerable server to a LAN, the internet, or a public hosting service.
- Use only dummy users, passwords, session data, and database records created for this lab.
- Never place real credentials, personal information, API keys, or reusable secrets in the project.
- Use Burp Suite, Wireshark, and similar tools only against this project and only when the user explicitly asks to run a test.
- Do not probe, scan, intercept, or attack third-party systems.
- Prefer demonstrations that are reversible and avoid destructive payloads, persistence, data exfiltration, or operating-system command execution.

## Change Discipline

- Read the relevant files before modifying them and keep changes narrowly scoped to the user's request.
- Preserve existing user work. Do not revert or overwrite unrelated changes.
- Do not edit files under `venv-secproject/`; treat the virtual environment as generated and replaceable.
- Treat `backups/` as read-only. Never modify an existing snapshot.
- Before a substantial change, explain what will be changed. Afterward, state what was changed and how it was verified.
- Ask before adding dependencies, changing the database design substantially, exposing a new network interface, or expanding the vulnerability scope.

## Vulnerable and Secure Implementations

- Confine deliberately vulnerable behavior to clearly named lab-only views, functions, URLs, or settings.
- Label vulnerable code with a short warning explaining that it exists only for the local demonstration.
- Provide a secure comparison for every vulnerable implementation.
- For SQL injection, keep unsafe raw SQL limited to the dedicated demonstration. Use Django's ORM or parameterized queries in the secure version.
- Do not weaken Django protections globally when a narrowly scoped demonstration is sufficient.
- Keep CSRF protection enabled unless a specific, documented experiment requires otherwise.
- For session testing, use a dummy account and demonstrate only the minimum behavior needed to compare cookie and transport protections.
- Make insecure and secure modes visibly distinguishable.

## Network and Tooling Rules

- Default Django binding: `127.0.0.1`. Do not use `0.0.0.0` for the vulnerable lab without explicit approval.
- Keep Burp's target scope restricted to this local application before sending any test requests.
- Explain that a trusted local Burp certificate allows the proxy to inspect HTTPS traffic; this does not show that TLS itself has been broken.
- Use Wireshark only to compare authorized local HTTP and HTTPS traffic, with no collection of unrelated credentials or traffic.

## Verification

- Run relevant Django checks and focused tests after code changes.
- Confirm that secure examples reject the matching vulnerable input or behavior.
- Confirm that test data contains no real credentials or personal information.
- If a check or demonstration cannot be run, say so clearly rather than claiming it succeeded.

