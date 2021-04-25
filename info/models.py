from django.db import models

class StockBasic(models.Model):

    symbol = models.IntegerField()
    name = models.CharField(max_length=150)
    capital = models.IntegerField()
    industry = models.CharField(max_length=150)
    listed_date = models.DateField()

class StockPrice(models.Model):

    date = models.DateField()
    symbol = models.IntegerField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    shares = models.IntegerField()
    volume = models.IntegerField()
    pe = models.FloatField()
    pb = models.FloatField()
    yield_rate = models.FloatField()

class StockChips(models.Model):

    date = models.DateField()
    symbol = models.IntegerField()
    margin_purchase = models.IntegerField()
    short_sale = models.IntegerField()
    foreign	 = models.IntegerField()
    trust = models.IntegerField()
    dealer = models.IntegerField()
    ftd_total = models.IntegerField()
