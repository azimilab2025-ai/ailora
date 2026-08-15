# Deployment and rollback runbook

Status: `LOCAL_QUALIFICATION_ONLY`; deployment requires `PRODUCTION_AUTHORIZATION_REQUIRED`.

Preflight: immutable commit, clean tree, pinned dependencies/actions, migrations, tests, package digest, secrets injected externally, Oya disabled, and approved change window. Local smoke checks configuration, health markers, dependency ordering and disabled auto-deploy without network traffic.

Rollback dry-run: identify previous immutable artifact, validate compatible database boundary, rehearse configuration rollback locally, preserve audit evidence, and stop on destructive migration or unknown data compatibility. This command performs no cloud, DNS, provider, credential, paid, NASA, Oya or production action.
