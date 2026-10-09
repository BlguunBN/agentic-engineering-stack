---
name: terraform-iac-suite
description: "Master unified Terraform & Infrastructure as Code (IaC) suite. Unifies Terraform multi-cloud patterns (AWS, Azure, GCP), Terragrunt DRY architecture, OpenTofu migration, and state locking/backend management."
use_when: "Reviewing or changing Terraform, Terragrunt, or OpenTofu configuration."
avoid_when: "Applying infrastructure changes without explicit authorization and rollback context."
entry_inputs: "Provider/backend, affected resources, state context, plan, and approval boundary."
workflow: "Inspect configuration/state safely, plan changes, validate, request approval before apply."
verification: "Run formatting, validation, and plan; never infer apply success from planning."
exit_output: "IaC diff, plan summary, risks, and explicit apply status."
category: "cloud-and-security"
tools:
  - terraform
  - terragrunt
  - opentofu
---

# Terraform & IaC Suite (Unified Master Skill)

A unified guide for declarative Infrastructure as Code across cloud providers using Terraform, OpenTofu, and Terragrunt.

## 1. Architecture Decision Ladder

```
[Need to provision cloud infrastructure]
   |
   +---> Managing single environment or simple multi-cloud resources?
   |        └──> Use standard Terraform / OpenTofu root modules with remote S3/GCS/Azure backend.
   |
   +---> Managing complex multi-account / multi-environment setups (dev/stage/prod across regions)?
   |        └──> Use `terragrunt-generator` (DRY configuration, automatic backend/provider inheritance).
   |
   +---> Migrating from HashiCorp Terraform to open-source OpenTofu?
            └──> Use `opentofu-migration` (verify 100% state compatibility, registry redirects).
```

## 2. Universal IaC Invariants (Ponytail / Safety)

1. **Remote State with Locking:** Never use local state for shared infrastructure. Always use S3 + DynamoDB, Azure Blob with lease, or GCS with object locking.
2. **Explicit Provider Constraints:** Pin provider versions with `~>` to avoid breaking changes on `terraform init`.
3. **Plan Before Apply:** Always review `terraform plan` output before applying changes. Check for unexpected resource destructions (`-/+`).
4. **Tagging Policy:** Enforce `Environment`, `Owner`, `Project`, and `ManagedBy = "terraform"` tags across all resources.

## 3. Production Module Skeleton

```hcl
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket         = "my-terraform-state-bucket"
    key            = "prod/app/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-lock"
  }
}

provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      ManagedBy   = "terraform"
      Environment = var.environment
    }
  }
}
```
