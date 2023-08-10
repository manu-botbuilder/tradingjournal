from django.shortcuts import render, redirect
from .forms import TradingPlanForm, TradeForm, TradeScreenshotForm
from .models import TradingPlan, Trade, DailySummary
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import json
import random
import calendar
from datetime import datetime, timedelta

from .chart import colorSuccess, colorDanger


def trading_plan(request):
    if request.method == 'POST':
        form = TradingPlanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('trading_plan')
    else:
        form = TradingPlanForm()

    plans = TradingPlan.objects.all()
    context = {
        'form': form,
        'plans': plans,
    }
    return render(request, 'trading_journal_app/trading_plan.html', context)


def trades(request):
    if request.method == 'POST':
        trade_form = TradeForm(request.POST)
        screenshot_form = TradeScreenshotForm(request.POST, request.FILES)

        if trade_form.is_valid() and screenshot_form.is_valid():
            trade = trade_form.save()
            screenshot = screenshot_form.save(commit=False)
            screenshot.trade = trade
            screenshot.save()
            return redirect('trades')
    else:
        trade_form = TradeForm()
        screenshot_form = TradeScreenshotForm()

    trades = Trade.objects.all()

    total_profits = 0
    profits = []
    profit_count = 0
    total_loss = 0
    losses = []
    loss_count = 0
    total_trades = len(trades)
    for trade in trades:
        if trade.profit_loss > 0:
            total_profits = total_profits + trade.profit_loss
            profits.append(int(trade.profit_loss))
            profit_count = profit_count + 1
        else:
            total_loss = total_loss + trade.profit_loss
            losses.append(int(trade.profit_loss))
            loss_count = loss_count + 1
    profit_percent = (profit_count / total_trades) * 100
    profit_s = sorted(profits)
    losse_s = sorted(losses)

    max_profit = profit_s[len(profit_s) - 1]
    max_loss = losse_s[0]
    total_pnl = total_profits + total_loss

    total_trades = len(trades)

    # Profit loss per day calculation
    profit_loss_dict = {}
    # Initial date
    initial_date = trades[total_trades - 1].date

    end_date = trades[0].date

    current_date = initial_date
    end_date = end_date + timedelta(days=1)
    while current_date < end_date:
        formatted_date = datetime.strptime(str(current_date), "%Y-%m-%d %H:%M:%S%z")
        # Format the date
        from_date = formatted_date.strftime("%Y-%m-%d 00:00:00+00:00")
        from_date_formatted = datetime.strptime(str(from_date), "%Y-%m-%d %H:%M:%S%z")
        to_date = formatted_date.strftime("%Y-%m-%d 23:59:59+00:00")
        to_date_formatted = datetime.strptime(str(to_date), "%Y-%m-%d %H:%M:%S%z")
        date_only_format = formatted_date.strftime("%Y-%m-%d")
        all_trades = Trade.objects.all()
        trades_for_date = all_trades.filter(date__range=[from_date_formatted,to_date_formatted])
        for trade in trades_for_date:
            #print(trade.profit_loss)
            if date_only_format in profit_loss_dict:
                profit_loss_dict[date_only_format] += trade.profit_loss
            else:
                profit_loss_dict[date_only_format] = trade.profit_loss

        current_date += timedelta(days=1)

    print(profit_loss_dict)
    total_profits_day = 0
    profits_day = []
    profit_count_day = 0
    total_loss_day = 0
    losses_day = []
    loss_count_day = 0
    total_trades_day = len(profit_loss_dict)
    for key, value in profit_loss_dict.items():
        if value > 0:
            total_profits_day = total_profits_day + value
            profits_day.append(int(value))
            profit_count_day = profit_count_day + 1
        else:
            total_loss_day = total_loss_day + value
            losses_day.append(int(value))
            loss_count_day = loss_count_day + 1
    profit_percent_day = (profit_count_day / total_trades_day) * 100
    profit_s_day = sorted(profits_day)
    losse_s_day = sorted(losses_day)

    max_profit_day = profit_s_day[len(profit_s_day) - 1]
    max_loss_day = losse_s_day[0]
    total_pnl_day = total_profits_day + total_loss_day

    context = {
        'trade_form': trade_form,
        'screenshot_form': screenshot_form,
        'trades': trades,
        'profit_percent': profit_percent,
        'profit_count': profit_count,
        'loss_count': loss_count,
        'loss': total_loss,
        'profits': total_profits,
        'max_profit': max_profit,
        'max_loss': max_loss,
        'total_pnl': total_pnl,
        'profit_percent_day': profit_percent_day,
        'profit_count_day': profit_count_day,
        'loss_count_day': loss_count_day,
        'loss_day': total_loss_day,
        'profits_day': total_profits_day,
        'max_profit_day': max_profit_day,
        'max_loss_day': max_loss_day,
        'total_pnl_day': total_pnl_day
    }
    return render(request, 'trading_journal_app/trades.html', context)


def trade_charts(request):
    trades = Trade.objects.all()
    profit_count = len([trade for trade in trades if trade.profit_loss > 0])
    loss_count = len([trade for trade in trades if trade.profit_loss < 0])

    labels_pie = ['Profit', 'Loss']
    values_pie = [profit_count, loss_count]

    # Generating random data for demonstration purposes (replace with actual data from trades)
    dates_line = [f'Day {i}' for i in range(1, 11)]
    profits_line = [random.randint(100, 1000) for _ in range(10)]
    losses_line = [random.randint(-1000, -100) for _ in range(10)]

    strategies = ['Strategy A', 'Strategy B', 'Strategy C']
    profits_bar = [random.randint(100, 1000) for _ in range(3)]
    losses_bar = [random.randint(-1000, -100) for _ in range(3)]

    entry_prices = [random.randint(100, 500) for _ in range(50)]
    exit_prices = [entry + random.randint(-50, 50) for entry in entry_prices]

    profits_histogram = [random.randint(100, 1000) for _ in range(30)]
    losses_histogram = [random.randint(-1000, -100) for _ in range(20)]

    # Candlestick Chart Data
    dataset_candlestick = []
    for entry, exit in zip(entry_prices, exit_prices):
        candlestick_data = {
            't': '2023-07-31',  # Replace with the actual date for the trade
            'o': entry + random.randint(-50, 50),
            'h': entry + random.randint(0, 100),
            'l': entry + random.randint(-100, 0),
            'c': exit,
        }
        dataset_candlestick.append(candlestick_data)

    # Area Chart Data
    cumulative_profits = [sum(profits_line[:i + 1]) for i in range(len(profits_line))]
    cumulative_losses = [sum(losses_line[:i + 1]) for i in range(len(losses_line))]

    # Update the context to include data for all the charts
    context = {
        'labels_pie': json.dumps(labels_pie),
        'values_pie': json.dumps(values_pie),
        'dates_line': json.dumps(dates_line),
        'profits_line': json.dumps(profits_line),
        'losses_line': json.dumps(losses_line),
        'strategies': json.dumps(strategies),
        'profits_bar': json.dumps(profits_bar),
        'losses_bar': json.dumps(losses_bar),
        'entry_prices': json.dumps(entry_prices),
        'exit_prices': json.dumps(exit_prices),
        'profits_histogram': json.dumps(profits_histogram),
        'losses_histogram': json.dumps(losses_histogram),
        'candlestick_dataset': json.dumps(dataset_candlestick),
        'cumulative_profits': json.dumps(cumulative_profits),
        'cumulative_losses': json.dumps(cumulative_losses),
    }

    return render(request, 'trading_journal_app/trade_charts.html', context)


def dashboard(request):
    # Calculate daily summary here (total_profit_loss) and save it to the DailySummary model
    # You can use the Trade model to retrieve the trades for a specific day and calculate the total profit/loss

    summaries = Trade.objects.all()

    context = {
        'summaries': summaries,
    }

    return render(request, 'trading_journal_app/Dashboard.html', context)


def trade_detail(request, pk):
    trade = get_object_or_404(Trade, pk=pk)
    labels = ['Profit', 'Loss']
    values = [1 if trade.profit_loss > 0 else 0, 1 if trade.profit_loss < 0 else 0]

    context = {
        'trade': trade,
        'labels_json': json.dumps(labels),
        'values_json': json.dumps(values),
    }
    return render(request, 'trading_journal_app/trade_detail.html', context)


def edit_trade(request, pk):
    trade = get_object_or_404(Trade, pk=pk)

    if request.method == 'POST':
        trade_form = TradeForm(request.POST, instance=trade)
        screenshot_form = TradeScreenshotForm(request.POST, request.FILES)

        if trade_form.is_valid() and screenshot_form.is_valid():
            trade = trade_form.save()
            screenshot = screenshot_form.save(commit=False)
            screenshot.trade = trade
            screenshot.save()
            return redirect('trades')
    else:
        trade_form = TradeForm(instance=trade)
        screenshot_form = TradeScreenshotForm()

    context = {
        'trade_form': trade_form,
        'screenshot_form': screenshot_form,
        'trade': trade,
    }
    return render(request, 'trading_journal_app/edit_trade.html', context)


def profit_loss_calendar(request):
    trades = Trade.objects.all()
    profit_loss_dict = {}
    total_trades = len(trades)
    initial_date = trades[total_trades - 1].date

    end_date = trades[0].date

    current_date = initial_date
    end_date = end_date + timedelta(days=1)
    while current_date < end_date:
        formatted_date = datetime.strptime(str(current_date), "%Y-%m-%d %H:%M:%S%z")
        # Format the date
        from_date = formatted_date.strftime("%Y-%m-%d 00:00:00+00:00")
        from_date_formatted = datetime.strptime(str(from_date), "%Y-%m-%d %H:%M:%S%z")
        to_date = formatted_date.strftime("%Y-%m-%d 23:59:59+00:00")
        to_date_formatted = datetime.strptime(str(to_date), "%Y-%m-%d %H:%M:%S%z")
        date_only_format = formatted_date.strftime("%Y-%m-%d")
        all_trades = Trade.objects.all()
        trades_for_date = all_trades.filter(date__range=[from_date_formatted, to_date_formatted])
        for trade in trades_for_date:
            # print(trade.profit_loss)
            if date_only_format in profit_loss_dict:
                profit_loss_dict[date_only_format] += trade.profit_loss
            else:
                profit_loss_dict[date_only_format] = trade.profit_loss

        current_date += timedelta(days=1)

    print(profit_loss_dict)
    context = {
        'profit_loss_dict': profit_loss_dict
    }

    return render(request, 'trading_journal_app/profit_loss_calendar.html', context)
