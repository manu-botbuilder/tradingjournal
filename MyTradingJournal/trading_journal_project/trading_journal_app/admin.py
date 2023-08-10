from django.contrib import admin
from .models import TradingPlan,Trade,DailySummary,TradeScreenshot
# Register your models here.
admin.site.register(TradingPlan)

admin.site.register(Trade)
# class tradeadmin(admin.ModelAdmin):
#     list_display = ("profit_loss",)  # author_email value is coming from below
#
#     def profit_loss(self, obj):  # You can create a custom method and show it in the 'list_display'
#         return obj.profit_loss


admin.site.register(DailySummary)
admin.site.register(TradeScreenshot)

