from helper import utils
import requests
import tempfile


class FileService:
    @staticmethod
    def read_local_csv(file_path):
        return utils.read_csv(file_path)

    @staticmethod
    def read_remote_csv(url):
        response = requests.get(url)
        response.raise_for_status()
        csv_data = response.text

        with tempfile.NamedTemporaryFile(
            mode="w+", delete=False, suffix=".csv"
        ) as tmp_file:
            tmp_file.write(csv_data)
            tmp_file.flush()
            temp_file_path = tmp_file.name

        return utils.read_csv(temp_file_path)
