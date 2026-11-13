```
I need to understand two things. Read-only: investigate and explain in plain language, don't change code.

Context, MartinAI architecture (from Jitesh, MartinAI team):
- Browser → Elastic Load Balancer → Chat-UI (Martin Chat, AWS EKS pod)
- Auth: Board Okta (OIDC), Chat-UI gets a JWT / id token
- Conversations stored in DocumentDB
- Chat-UI → LiteLLM proxy (AI inference proxy, EKS pod; keys/spend/model config in Postgres) → AWS Bedrock (Claude, Llama, Titan, Cohere). LiteLLM standardizes requests and responses.
- LiteLLM has DEV, TEST and PROD servers. MartinAI calls the LiteLLM API with the Bedrock model named in the request.
- Logs: CloudWatch (model invocation logs expire after 30 days), Splunk gets container/system/app logs but no model invocation logs.
- SkillHub runs on-prem (fweb, Apache/CGI, Kerberos auth), not in AWS.

Part 1: LLM scan reviewer status
1. List what's done (by stage), what's left, and what's blocked. Include the DLP-blocked pieces (scripts/run_llm_review.py, worker, CLI, enqueue endpoint; InfoSec exception pending for event dlp_7edb32a41739), migration 062, the open design decisions, and the known bugs (run_gate2_scan status enum, etc.).
2. For each remaining piece: what it does, its size (S/M/L), and its dependencies.
3. Map the reviewer onto LiteLLM: which environment SkillHub dev/prod should use (DEV/TEST/PROD), what kind of key (a LiteLLM virtual key per environment, with a budget and allowed models), which model name format to send, and how the reviewer should handle LiteLLM errors, timeouts and rate limits.

Part 2: MartinAI integration
1. Explain the two possible meanings: (A) SkillHub's reviewer calls MartinAI's LiteLLM gateway, and (B) MartinAI users discover and use SkillHub skills.
2. For (B), compare these options using what's actually in our repo:
   - a read-only SkillHub REST API (e.g. list/search published skills, get skill content by slug/version)
   - our existing SkillHub MCP server (find it, show its tools such as get_skill, and say whether MartinAI's Chat-UI could call it)
   For each: endpoints/tools needed, what data is exposed (published and approved skills only? division rules?), and auth. Note that MartinAI uses Okta OIDC JWTs while SkillHub uses Kerberos. Propose service-to-service auth options.
3. Network: MartinAI runs in AWS EKS and SkillHub on-prem. List what must be true for one to reach the other (direction of calls, firewall, proxies). Don't assume. Mark what needs confirming.
4. Recommend one approach for (B) with a short phased plan (MVP first), plus a sequence diagram in Mermaid for both (A) and (B).
5. Give me a list of questions to ask Jitesh and the MartinAI team, and anything that needs Information Security sign-off (e.g. submission text going to Bedrock, invocation logging).

Format: a short plain-language summary first, then the details. Don't print secrets, keys or tokens.
```
