from helper import utils


class HistoricDataService:
    @staticmethod
    def get_historic_data(order_id, interval="4h"):
        order = utils.get_order(order_id)
        return order.adapter.get_historic_data(order.asset, interval)
