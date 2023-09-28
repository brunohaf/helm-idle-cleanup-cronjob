from azure.storage.fileshare import ShareFileClient
import json

class AzureShareFileService:
    def __init__(
        self,
        conn_str: str = None,
        share_name: str = None
    ):
        if conn_str is None or share_name is None:
            raise TypeError("missing conn_str or share_name")

        self.conn_str = conn_str
        self.share_name = share_name

    def upload_json_file(self, file_path: str, file: dict):
        azure_file_client = ShareFileClient.from_connection_string(
            conn_str=self.conn_str,
            share_name=self.share_name,
            file_path=file_path)
        azure_file_client.upload_file(json.dumps(file))
