from django.contrib import admin
from .models import StockPrice, StockBasic, StockChips

admin.site.register(StockPrice)
admin.site.register(StockBasic)
admin.site.register(StockChips)
