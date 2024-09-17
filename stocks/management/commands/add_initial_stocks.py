from django.core.management.base import BaseCommand
from stocks.models import Stock


class Command(BaseCommand):
    help = "Add initial stock data"

    def handle(self, *args, **kwargs):
        initial_stocks = [
            {"ticker": "AAPL", "name": "Apple Inc.", "price": 0.00},
            {"ticker": "GOOGL", "name": "Alphabet Inc.", "price": 0.00},
            {"ticker": "MSFT", "name": "Microsoft Corporation", "price": 0.00},
        ]
        for stock_data in initial_stocks:
            stock, created = Stock.objects.get_or_create(
                ticker=stock_data["ticker"],
                defaults={"name": stock_data["name"], "price": stock_data["price"]},
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added {stock.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"{stock.name} already exists"))
