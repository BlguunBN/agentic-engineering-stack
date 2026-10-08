---
name: docker-containers-suite
description: "Master unified Docker & containerization suite. Covers multi-stage Dockerfiles, image layer caching, security hardening (distroless, non-root), Docker Compose architectures, and local development setups."
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

## 2. Production Multi-Stage Dockerfile Template (Node/TypeScript)

```dockerfile
# Stage 1: Build & Dependencies
FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build && npm prune --production

# Stage 2: Minimal Distroless / Hardened Runtime
FROM node:22-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production

# Security: Non-root user
USER node

COPY --from=builder --chown=node:node /app/node_modules ./node_modules
COPY --from=builder --chown=node:node /app/dist ./dist
COPY --from=builder --chown=node:node /app/package.json ./package.json

EXPOSE 3000
CMD ["node", "dist/index.js"]
```

## 3. Container Hardening Checklist (`container-security-hardening`)

- [ ] `.dockerignore` exists (excludes `.git`, `node_modules`, `.env`, test files).
- [ ] Application runs under explicit non-root UID/GID.
- [ ] Base image uses pinned minimal tags (`alpine` or distroless).
- [ ] No secrets or build credentials baked into layers.
- [ ] Explicit health checks configured on services.
