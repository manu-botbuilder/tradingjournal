from django import forms
from .models import TradingPlan, Trade, TradeScreenshot

class TradingPlanForm(forms.ModelForm):
    class Meta:
        model = TradingPlan
        fields = ['date', 'plan']

class TradeForm(forms.ModelForm):
    class Meta:
        model = Trade
        fields = ['date', 'entry_price', 'exit_price', 'reason', 'profit_loss', 'instrument', 'trade_type', 'quantity']

class TradeScreenshotForm(forms.ModelForm):
    class Meta:
        model = TradeScreenshot
        fields = ['screenshot']
