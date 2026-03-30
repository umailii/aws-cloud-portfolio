# Cloud Web Application Architecture (AWS)
> ITSS 3300 | University of Texas at Dallas | July 2025  
> **Author:** Umair Ali

A documented cloud architecture project designing a scalable, fault-tolerant web application on AWS. This project focuses on architectural decisions, service selection, security best practices, and cost awareness — not just getting something working, but understanding *why* each design choice was made.

---

## Architecture Overview

```
                        ┌─────────────────────────────────────┐
                        │             AWS VPC                  │
                        │                                      │
User ──────────────▶  ALB  ──────────▶  EC2 Instance 1        │
                        │          └──▶  EC2 Instance 2        │
                        │                    │                 │
                        │                    ▼                 │
                        │              S3 Bucket               │
                        │           (Static Assets)            │
                        │                                      │
                        │  IAM Roles control all access        │
                        └─────────────────────────────────────┘
```

---

## Services Used

| Service | Role | Why |
|---------|------|-----|
| **EC2** | Web + application servers | Full control over compute environment |
| **S3** | Static file storage | Purpose-built object storage, scales automatically |
| **IAM** | Access control | Least-privilege security across all services |
| **Application Load Balancer** | Traffic distribution | Fault tolerance and high availability |

---

## Key Design Decisions

- **Two EC2 instances** behind the load balancer for redundancy — if one fails, traffic routes to the other automatically
- **Static assets on S3** rather than EC2, reducing compute load and simplifying deployments
- **IAM roles** assigned to EC2 instead of hardcoded credentials — no keys stored in application code
- **ALB health checks** continuously verify instance availability and reroute traffic on failure

Full decision rationale is documented in [`ARCHITECTURE_DECISIONS.md`](./ARCHITECTURE_DECISIONS.md)

---

## What I Learned

- How to design for **fault tolerance** — eliminating single points of failure
- The difference between **availability** and **scalability** and how this architecture addresses both
- Why **IAM least privilege** matters and how to apply it practically
- How **request flow** works through a load-balanced, multi-tier application
- How to evaluate **cost tradeoffs** — S3 for static assets significantly reduces EC2 load at scale

---

## Architectural Diagrams

All data flows, service roles, and design patterns are documented in the architecture decisions file. This project included 10+ documented decisions covering security, availability, scalability, and cost.

---

*Part of the [AWS Cloud Portfolio](https://github.com/umailii/aws-cloud-portfolio) — a collection of hands-on AWS projects built during my CIST degree at UTD.*
