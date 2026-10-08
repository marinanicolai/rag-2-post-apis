```
Analyze the current architecture of this  application.

Context:
 is an internal application built with React, Flask/Python, PostgreSQL, and Redis. It uses Kerberos SSO authentication with session tokens and is deployed through GitLab CI.

Investigate:
1. The overall repository structure and major components.
2. React frontend organization and how it communicates with the backend.
3. Flask API structure, blueprints, routes, and service layers.
4. PostgreSQL connections, ORM models, and migration framework.
5. Redis usage, including caching, sessions, and background jobs.
6. Authentication and authorization flow.
7. GitLab CI/CD deployment process.
8. Existing integrations with external services.

Produce:
- A high-level architecture overview.
- A Mermaid component diagram showing how the components communicate.
- A list of important files and directories with their purpose.
- An explanation of the application's current data flow.
- Existing architectural limitations relevant to implementing a secure plugin approval and distribution workflow.

Use only verified repository evidence. Include file paths and line numbers where possible. Mark anything that cannot be determined as UNKNOWN.

Do not modify any files or configurations.

```
