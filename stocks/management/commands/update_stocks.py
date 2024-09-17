from django.core.management.base import BaseCommand
from stocks.models import Stock
from stocks_processing.fetch_stocks import fetch_stock_data
from datetime import datetime


class Command(BaseCommand):
    help = "Update stock prices"

    def handle(self, *args, **kwargs):
        stocks = Stock.objects.all()
        for stock in stocks:
            data = fetch_stock_data(stock.ticker)
            stock.last_time_updated = self._get_closest_valid_time(data)
            # TODO fetch time series with different update frequency
            # TODO fetch different open/close values
            stock.price = data["Time Series (1min)"][
                stock.last_time_updated.strftime("%Y-%m-%d %H:%M:%S")
            ]["4. close"]
            stock.save()
            self.stdout.write(self.style.SUCCESS(f"Updated {stock.name}"))

    def _get_closest_valid_time(self, stock_data):
        all_times = [
            datetime.strptime(key, "%Y-%m-%d %H:%M:%S")
            for key in stock_data["Time Series (1min)"].keys()
        ]
        return min(all_times, key=lambda time: abs(time - datetime.now()))
