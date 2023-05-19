## Helm Release Resource Optimizer

The Helm Release Resource Optimizer is a solution designed to remove inactive releases and optimize computational resources. It leverages Kubernetes' cronjob functionality to periodically evaluate Helm releases and delete those whose services that have shown no activity for a specified period of time, resulting in cost savings and improved resource utilization.

This repository contains the code and Helm charts required to deploy the resource optimizer as a cronjob in a Kubernetes cluster. The cronjob executes a Python script that interacts with Prometheus and Helm to identify inactive releases and initiate their removal. Email notifications are sent out for each deleted release, providing visibility and accountability.

### Key Features

- Automated removal of inactive Helm releases
- Resource optimization and cost savings
- Integration with Prometheus for release activity monitoring
- Email notifications for release deletions
- Easy deployment using Helm charts

By leveraging this Helm Release Resource Optimizer, organizations can efficiently manage their Helm releases, ensure resource efficiency, and enhance cost-effectiveness in their Kubernetes environments.