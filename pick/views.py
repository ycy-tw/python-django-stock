from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from info.models import StockPrice, StockChips, StockBasic
from django.contrib.auth.decorators import login_required

import pandas as pd
import json
import csv
import codecs

price_column = [
    'pe', 'pb', 'yield_rate',
]

chips_column = [
    'margin_purchase', 'short_sale', 'foreign',
    'trust', 'dealer', 'ftd_total',
]


def get_symbol_name(symbols):
    names = dict(StockBasic.objects.filter(
        symbol__in=symbols).values_list('symbol', 'name'))
    return {'證券名稱': names}


def col_name_to_var(variable):

    col_to_chinese = {
        'pe': '本益比',
        'pb': '股價淨值比',
        'yield_rate': '現金殖利率(%)',
        'margin_purchase': '融資',
        'short_sale': '融券',
        'foreign': '外資',
        'trust': '投信',
        'dealer': '自營',
        'ftd_total': '三大法人',
    }

    return col_to_chinese[variable]


# Create your views here.
def var_to_col(variable):

    chinese_to_col = {
        '本益比': 'pe',
        '股價淨值比': 'pb',
        '現金殖利率': 'yield_rate',
        '融資': 'margin_purchase',
        '融券': 'short_sale',
        '外資': 'foreign',
        '投信': 'trust',
        '自營': 'dealer',
        '三大法人': 'ftd_total',
    }

    return chinese_to_col[variable]


def chips_condition(df, condition):

    firm_attr = list(condition.keys())[0]
    more_or_less, threshold = condition[firm_attr]

    df = df[['date', 'symbol', firm_attr]]
    df.date = pd.to_datetime(df.date)
    df = df.set_index(['date', 'symbol']).unstack()
    df.columns = df.columns.droplevel()
    df = df.groupby(pd.Grouper(level='date', freq='M')).sum().iloc[-int(threshold):, :]

    qualified_symbols = set(df.columns[(df > 0).all() == True]) if more_or_less in ['大於', '增加', '買超'] \
        else set(df.columns[(df < 0).all() == True])

    qualified_symbols_value = df[qualified_symbols].sum().to_dict()
    firm_attr_result = {
        f'{col_name_to_var(firm_attr)}近{threshold}個月累積(張)': qualified_symbols_value}

    return qualified_symbols, firm_attr_result


def basic_condition(df, condition):

    firm_attr = list(condition.keys())[0]
    more_or_less, threshold = condition[firm_attr]
    latest_date = df.date.max()
    df = df[df.date == latest_date][['symbol', firm_attr]]
    df.set_index('symbol', inplace=True)

    if more_or_less == '大於':
        qualified_symbols = set(
            df[(df[firm_attr] >= float(threshold)) == True].index)

    elif more_or_less == '小於':
        qualified_symbols = set(
            df[(df[firm_attr] < float(threshold)) == True].index)

    qualified_symbols_value = df[df.index.isin(list(qualified_symbols))][firm_attr].to_dict()
    firm_attr_result = {col_name_to_var(firm_attr): qualified_symbols_value}

    return qualified_symbols, firm_attr_result


def get_latest_stock_return(symbols):

    df = pd.DataFrame(StockPrice.objects.all().values())
    df.date = pd.to_datetime(df.date)
    df = df[['date', 'symbol', 'close']]
    latest_date = df.date.max()

    df = df.set_index(['date', 'symbol']).unstack()
    df.columns = df.columns.droplevel()
    df = df[df.index <= latest_date][symbols]

    latest_price = df.iloc[-1, :]
    last_20_price = df.iloc[-20, :]
    last_60_price = df.iloc[-60, :]
    last_120_price = df.iloc[-120, :]

    latest_price_return = {
        f'最新收盤價': latest_price.to_dict(),
        '近20天報酬率(%)': ((last_20_price / latest_price) - 1).to_dict(),
        '近60天報酬率(%)': ((last_60_price / latest_price) - 1).to_dict(),
        '近120天報酬率(%)': ((last_120_price / latest_price) - 1).to_dict(),
    }

    return latest_price_return


@login_required
def pick_view(request):

    global filter_result

    if 'conditions' in request.GET:

        conditions = json.loads(request.GET.get('conditions'))
        print(conditions)
        for firm_attr in list(conditions.keys()):
            conditions[var_to_col(firm_attr)] = conditions.pop(firm_attr)

        final_qualified_symbols = set(StockBasic.objects.values_list('symbol', flat=True))
        final_output_dict = {}

        for firm_attr in conditions:

            if (firm_attr in price_column):

                priceTable = pd.DataFrame(
                    StockPrice.objects
                    .filter(symbol__in=list(final_qualified_symbols))
                    .values('date', 'symbol', firm_attr)
                )
                qualified_symbols, firm_attr_result = basic_condition(priceTable, {firm_attr: conditions[firm_attr]})

            elif (firm_attr in chips_column):

                chipsTable = pd.DataFrame(
                    StockChips.objects.
                    filter(symbol__in=list(final_qualified_symbols))
                    .values('date', 'symbol', firm_attr)
                )
                qualified_symbols, firm_attr_result = chips_condition(chipsTable, {firm_attr: conditions[firm_attr]})

            # Once no result under one of the conditinos, means no qualified symbols.
            if (len(qualified_symbols) == 0):

                final_qualified_symbols = set()
                final_output_dict = {}
                break

            else:

                final_qualified_symbols = final_qualified_symbols & qualified_symbols
                final_output_dict.update(firm_attr_result)

        if len(final_qualified_symbols) != 0:

            latest_price_return = get_latest_stock_return(final_qualified_symbols)
            symbols_names = get_symbol_name(final_qualified_symbols)
            latest_price_return.update(final_output_dict)
            symbols_names.update(latest_price_return)

            filter_result = pd.DataFrame(symbols_names).round(2)
            filter_result.index.name = '證券代號'
            filter_result = filter_result[filter_result.index.isin(final_qualified_symbols)]
            filter_result.reset_index(inplace=True)

            filter_result = filter_result.T.to_dict()

            '''
            {0: {'證券代號': 1101, '證券名稱': '台泥', '最新收盤價': 47.2,
            '近20天報酬率(%)': -0.1, '近60天報酬率(%)': -0.09, '近120天報酬率(%)': -0.14,
            '本益比': 11.16}, 1: {'證券代號': 1102, '證券名稱': '亞泥', '最新收盤價': 47.35,
            '近20天報酬率(%)': -0.08, '近60天報酬率(%)': -0.09, '近120天報酬率(%)': -0.14, '本益比': 10.81},
            '''

        elif len(final_qualified_symbols) == 0:
            filter_result = {}

        print('+----------------------+')
        print('|  Success Call Back!  |')
        print('+----------------------+')

        return JsonResponse({'conditionResult': filter_result}, status=200)

    return render(request, 'pick/pick.html')


def download_pick_result(request):

    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    response.write(codecs.BOM_UTF8)  # for chinese encoding problem

    try:
        writer.writerow(list(filter_result.columns))
        for i in range(len(filter_result)):
            writer.writerow(list(filter_result.loc[i].values))

        response['Content-Disposition'] = 'attachment; filename="result.csv"'

    except:
        response['Content-Disposition'] = 'attachment; filename="result.csv"'

    return response
