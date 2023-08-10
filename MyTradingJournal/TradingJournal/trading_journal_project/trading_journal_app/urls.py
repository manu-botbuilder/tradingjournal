from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('trading_plan/', views.trading_plan, name='trading_plan'),
    path('trades/', views.trades, name='trades'),
    path('', views.dashboard, name='dashboard'),
    path('trade/<int:pk>/', views.trade_detail, name='trade_detail'),
    path('edit_trade/<int:pk>/', views.edit_trade, name='edit_trade'),
    path('trade_charts/', views.trade_charts, name='trade_charts'),
    path('profit_loss_calendar/', views.profit_loss_calendar, name='profit_loss_calendar'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)