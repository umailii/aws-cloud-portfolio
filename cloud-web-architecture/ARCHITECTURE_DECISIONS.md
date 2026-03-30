# Architectural Decision Records (ADR)
**Project:** Scalable Web Application on AWS  
**Course:** ITSS 3300 | University of Texas at Dallas  
**Author:** Umair Ali  
**Date:** July 2025

---

## ADR-001: Use EC2 for Application Hosting

**Decision:** Host the web application on Amazon EC2 instances rather than a managed service like Elastic Beanstalk.

**Reasoning:** EC2 gives full control over the server environment, OS configuration, and software stack. For a learning-focused project, this was the right choice because it exposes the underlying infrastructure rather than abstracting it away.

**Tradeoff:** More manual configuration required compared to a managed service, but deeper understanding of how the compute layer works.

---

## ADR-002: Use Application Load Balancer for Traffic Distribution

**Decision:** Place an Application Load Balancer (ALB) in front of the EC2 instances to distribute incoming traffic.

**Reasoning:** A single EC2 instance creates a single point of failure. The ALB distributes requests across multiple instances, meaning if one server goes down, traffic is automatically routed to the healthy one. This directly addresses the fault tolerance requirement.

**Tradeoff:** Adds cost and architectural complexity, but is essential for any production-grade web application.

---

## ADR-003: Use S3 for Static Asset Storage

**Decision:** Store all static files (HTML, CSS, JavaScript, images) in an S3 bucket rather than on the EC2 instances themselves.

**Reasoning:** S3 is purpose-built for object storage. Keeping static assets separate from the compute layer means the EC2 instances only handle dynamic application logic. This reduces load on the servers and makes deployments cleaner.

**Tradeoff:** Requires proper bucket policy configuration and CORS settings, which adds initial setup complexity.

---

## ADR-004: Use IAM for Access Control

**Decision:** Use IAM roles and policies to control which services can access which resources, rather than using root credentials or hardcoded keys.

**Reasoning:** Following the principle of least privilege — each service only gets the permissions it actually needs. The EC2 instances were assigned an IAM role with read/write access to the specific S3 bucket. No credentials are stored in application code.

**Tradeoff:** Requires upfront planning of permission boundaries, but eliminates the security risk of exposed credentials.

---

## ADR-005: Multi-Instance Deployment for Availability

**Decision:** Deploy two EC2 instances behind the load balancer rather than a single instance.

**Reasoning:** A single instance means any maintenance window, failure, or update causes downtime. Two instances allow rolling updates and provide redundancy. The ALB health checks automatically detect if an instance becomes unhealthy and stops sending traffic to it.

**Tradeoff:** Doubles the EC2 compute cost, but is the minimum viable setup for a highly available application.

---

## Request Flow Summary

```
User → Application Load Balancer → EC2 Instance (app logic)
                                 → S3 Bucket (static assets)
```

1. User sends an HTTP request to the ALB endpoint
2. ALB evaluates the health of both EC2 instances
3. ALB forwards the request to the healthiest available instance
4. If the request is for a static file, EC2 serves it directly from S3
5. If the request requires dynamic processing, EC2 handles it and returns a response

---

## Scalability Considerations

- **Horizontal scaling:** Additional EC2 instances can be added behind the ALB without changing the architecture
- **S3 scalability:** S3 scales automatically — no capacity planning required for static assets
- **Cost awareness:** Keeping static assets in S3 reduces the compute load on EC2, which directly reduces cost at scale
