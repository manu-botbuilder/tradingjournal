from django.db import models

class TradingPlan(models.Model):
    date = models.DateField()
    plan = models.TextField()

class Trade(models.Model):
    date = models.DateTimeField()
    instrument = models.CharField(max_length=100,default="NULL")
    type_choices = (
        ("Buy", "Buy"),
        ("Sell", "Sell"),
    )
    trade_type = models.CharField(max_length=255, choices=type_choices, default="Buy")
    quantity = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    entry_price = models.DecimalField(max_digits=10, decimal_places=2)
    exit_price = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField()
    profit_loss = models.DecimalField(max_digits=10, decimal_places=2)
    #last deleted entry is id=3
    class Meta:
        ordering = ['-date']
    def __str__(self):
        return str(self.date)
class DailySummary(models.Model):
    date = models.DateField()
    total_profit_loss = models.DecimalField(max_digits=10, decimal_places=2)

class TradeScreenshot(models.Model):
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE)
    screenshot = models.ImageField(upload_to='trade_screenshots/')
