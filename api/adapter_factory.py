from api.binance_api import BinanceAPI
import helper.utils


class AdapterFactory:
    @staticmethod
    def get_adapter(platform: str):
        if platform == "binance":
            creds = helper.utils.get_binance_api_credentials()
            return BinanceAPI(creds.get("api_key"), creds.get("api_secret"))
        # Add more platforms here as needed
        return None
