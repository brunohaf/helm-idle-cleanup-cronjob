# Slim version of 4n4nd's PrometheusConnect
# Available at https://github.com/4n4nd/prometheus-api-client-python

from urllib.parse import urlparse
import logging
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

# set up logging

_LOGGER = logging.getLogger(__name__)

# In case of a connection failure try 2 more times
MAX_REQUEST_RETRIES = 3
# wait 1 second before retrying in case of an error
RETRY_BACKOFF_FACTOR = 1
# retry only on these status
RETRY_ON_STATUS = [408, 429, 500, 502, 503, 504]

class PrometheusClient:
    def __init__(
        self,
        url: str = "http://prometheus:9090",
        retry: Retry = None
    ):
        if url is None:
            raise TypeError("missing url")

        self.url = url
        self.prometheus_host = urlparse(self.url).netloc

        if retry is None:
            retry = Retry(
                total=MAX_REQUEST_RETRIES,
                backoff_factor=RETRY_BACKOFF_FACTOR,
                status_forcelist=RETRY_ON_STATUS,
            )

        self._session = requests.Session()
        self._session.mount(self.url, HTTPAdapter(max_retries=retry))

    def custom_query(self, query: str, params: dict = None):
        params = params or {}
        data = None
        query = str(query)

        response = self._session.get(
            "{0}/api/v1/query".format(self.url),
            params={**{"query": query}, **params}
        )
        if response.status_code == 200:
            data = response.json()["data"]["result"]
        else:
            raise Exception(
                "HTTP Status Code {} ({!r})".format(response.status_code, response.content)
            )

        return data