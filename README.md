## Helm Idle Cleanup Cronjob

## ℹ️ About

The helm-idle-cleanup-cronjob project aims to implement a Kubernetes cronjob that runs periodically to identify and lift all Helm releases that have not received any requests in the last two weeks. The solution utilizes Prometheus to fetch the appropriate metrics before determining the release deletion.

The current version of the project has been developed to fetch metrics from the Kubernetes Ingress Controller Prometheus resource. This allows for the analysis of request metrics for all applications that have an ingress within the cluster. Presently, this version does not directly delete the releases; instead, it sends the list of releases to a Azure File Share. Subsequently, an 'Purger' Azure Pipeline retrieves this list and performs the releases deletion. The helm-idle-cleanup-cronjob will also get k8s cluster nodes' capacity/allocated info and also upload it to the fileshare.

## 🚀 Features

- Fetches volumetry on application ingress through the "nginx_ingress_controller_requests" metric from Monitoring Prometheus (refer to this [article on ingress-nginx metrics](https://kubernetes.github.io/ingress-nginx/user-guide/monitoring/)).
- Creates a list for purging only the applications whose deployment has the 'team' label associated with one of the CSPS teams.
- Logs purging events on Seq.
- Utilizes Azure FileShare as a file server and datalake for persistent logs.
- Enhance cost-effectiveness on Kubernetes clusters by automating the deletion of inactive Helm releases with the Purger Pipeline.

By leveraging this Helm Idle Cleanup Cronjob, organizations can efficiently manage their Helm releases, ensure resource efficiency, and enhance cost-effectiveness in their Kubernetes environments.
