from prometheus_api_client import PrometheusConnect
from subprocess import run
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta

# Prometheus Settings
prometheus_url = "http://prometheus:9090"
prometheus = PrometheusConnect(url=prometheus_url)

# Email settings
email_from = "your-email@example.com"
email_to = "email@teste.com"
smtp_server = "smtp.example.com"
smtp_port = 587
smtp_username = "your-email@example.com"
smtp_password = "your-password"

# Fetchs Helm releases
helm_releases = run(["helm", "list", "--short"], capture_output=True, text=True).stdout.strip().split("\n")

# Iterates through releases
for release in helm_releases:
    # Checks if there is a ServiceMonitor associated with the release
    service_monitor_query = f'servicemonitors{{{{release}}}}'
    service_monitor_results = prometheus.custom_query(service_monitor_query)
    if len(service_monitor_results) == 0:
        # ServiceMonitor not found, proceed to next release
        continue

    # Checks if there have been requests in the last 2 weeks
    two_weeks_ago = datetime.now() - timedelta(days=14)
    requests_query = f'sum(rate(http_requests_total{{job="{release}"}}[2w]))'
    requests_result = prometheus.custom_query(requests_query, start_time=two_weeks_ago)
    if len(requests_result) == 0 or requests_result[0]["value"][1] == "0":
        # There have been no requests in the last 2 weeks
        # Deletes Helm release
        #run(["helm", "delete", release])
        
        # Sends email notifying release deletion
        email_subject = f"Helm release {release} purged"
        email_body = f"The Helm release {release} was purged due to application inativity (lack of requests in the last 2 weeks)."
        msg = MIMEText(email_body)
        msg["Subject"] = email_subject
        msg["From"] = email_from
        msg["To"] = email_to
        smtp = smtplib.SMTP(smtp_server, smtp_port)
        smtp.starttls()
        smtp.login(smtp_username, smtp_password)
        smtp.send_message(msg)
        smtp.quit()
