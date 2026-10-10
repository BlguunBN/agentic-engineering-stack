---
name: docker-containers-suite
description: "Master unified Docker & containerization suite. Covers multi-stage Dockerfiles, image layer caching, security hardening (distroless, non-root), Docker Compose architectures, and local development setups."
use_when: "Creating, debugging, sizing, or hardening Docker images and Compose services."
avoid_when: "Changing orchestration beyond containers or editing app code unrelated to builds."
entry_inputs: "Application runtime, build/test commands, deployment constraints, and current container files."
workflow: "Inspect existing configuration, choose build/runtime stages, harden, build and test."
verification: "Build the image and inspect runtime user, secrets, health, and startup behavior."
exit_output: "Container changes with build and runtime verification results."
category: "cloud-and-security"
tools:
  - docker
  - docker-compose
---

# Docker Containers Suite (Unified Master Skill)

A comprehensive guide for containerization, production multi-stage builds, and container security.

## 1. Tool Selection Ladder

```
[Need container setup or troubleshooting]
   |
   +---> Creating a new Dockerfile?
   |        └──> Use Multi-Stage Build pattern (build dependencies in builder stage, copy artifacts to minimal runtime).
   |
   +---> Orchestrating multiple services locally (App + DB + Redis)?
   |        └──> Use `docker-compose` with healthchecks and named volumes.
   |
   +---> Preparing for production security audit?
   |        └──> Apply `container-security-hardening` (drop privileges, use non-root user, read-only rootfs).
   |
   +---> Debugging slow build times or large image sizes?
            └──> Audit layer caching order and add `.dockerignore`.
```

## 2. Production Multi-Stage Dockerfile Template

A Node/TypeScript example is available in [references/node-multistage-dockerfile.md](references/node-multistage-dockerfile.md). Adapt it to the actual runtime and verify the final image; the sample is not a universal production recipe.

## 3. Container Hardening Checklist (`container-security-hardening`)

- [ ] `.dockerignore` exists (excludes `.git`, `node_modules`, `.env`, test files).
- [ ] Application runs under explicit non-root UID/GID.
- [ ] Base image uses pinned minimal tags (`alpine` or distroless).
- [ ] No secrets or build credentials baked into layers.
- [ ] Explicit health checks configured on services.
