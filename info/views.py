from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from .models import StockPrice, StockBasic, StockChips

from datetime import datetime, timedelta
import pandas as pd
from bokeh.embed import components
from bokeh.plotting import figure, output_file, show
from bokeh.models import (
    LinearAxis,
    Range1d,
    DatetimeTickFormatter,
    ColumnDataSource,
    NumeralTickFormatter,
    HoverTool,
    TableColumn,
    DateFormatter,
    DataTable,
    Legend,
)
# https://docs.djangoproject.com/en/3.1/ref/templates/builtins/#std:templatetag-url

price_column = [
    'pe', 'pb', 'yield_rate',
]

chips_column = [
    'margin_purchase', 'short_sale', 'foreign',
    'trust', 'dealer', 'ftd_total',
]


def english_to_chinese(variable):

    eng_to_chi = {
        'pe': '本益比',
        'pb': '股價淨值比',
        'yield_rate': '殖利率',
        'margin_purchase': '融資增減',
        'short_sale': '融券增減',
        'foreign': '外資買賣超',
        'trust': '投信買賣超',
        'dealer': '自營買賣超',
        'ftd_total': '三大法人買賣超',
    }

    return eng_to_chi[variable]


def chinese_to_column_name(variable):

    chi_to_column_name = {
        '本益比': 'pe',
        '股價淨值比': 'pb',
        '現金殖利率': 'yield_rate',
        '融資增減': 'margin_purchase',
        '融券增減': 'short_sale',
        '外資買賣超': 'foreign',
        '投信買賣超': 'trust',
        '自營買賣超': 'dealer',
        '三大法人買賣超': 'ftd_total',
    }

    return chi_to_column_name[variable]


def bokeh_plotting(data, variable):

    data = data.groupby(pd.Grouper(key='date', freq='M')).mean().tail(36)
    CompanyVariable = data[variable]
    source = ColumnDataSource(data)
    # ---------------------------------------

    p = figure(
        plot_width=600,
        plot_height=350,
        x_axis_type='datetime'
    )

    p.toolbar.logo = None
    p.toolbar_location = None
    p.toolbar.active_drag = None
    # ---------------------------------------

    variablePlot = p.vbar(
        x='date',
        top=f'{variable}',
        width=timedelta(days=15),
        fill_alpha=0.5,
        color="#00B4D8",
        y_range_name="foo",
        source=source,
        # legend_label=f'{english_to_chinese(variable)}',
    )

    closePrice = p.line(
        x='date',
        y='close',
        width=3,
        color='#0077B6',
        source=source,
        # legend_label='收盤價',
    )

    # ---------------------------------------
    p.y_range = Range1d(min(data.close)*0.9, max(data.close)*1.1)
    p.yaxis[0].formatter = NumeralTickFormatter(format="$0")

    p.extra_y_ranges = {"foo": Range1d(
        start=min(CompanyVariable)*0.9, end=max(CompanyVariable)*1.1)}
    p.add_layout(LinearAxis(y_range_name="foo"), 'right')

    p.xaxis.formatter = DatetimeTickFormatter(months=['%Y-%m'])
    p.xaxis.major_label_overrides = {
        i: date.strftime('%b %d') for i, date in enumerate(data.index)
    }

    # ---------------------------------------
    legend = Legend(items=[(f'{english_to_chinese(variable)}', [variablePlot]),
                           ('月均價', [closePrice])],
                    location='center')

    legend.label_text_font_size = '8pt'
    legend.glyph_height = 14
    legend.click_policy = 'hide'
    legend.orientation = 'horizontal'

    p.add_layout(legend, 'below')
    # ‘left’, ‘right’, ‘above’, ‘below’, ‘center’

    # ---------------------------------------
    script, div = components(p)

    return data, script, div


@login_required
def basic_variable_view(request, symbol):

    if 'FirmAttr' in request.GET:

        variable = request.GET.get('FirmAttr')
        variable = chinese_to_column_name(variable)

        if variable in price_column:
            data = pd.DataFrame(
                StockPrice.objects.filter(symbol=symbol)
                .values_list('date', variable, 'close')
            )

        elif variable in chips_column:
            data = pd.DataFrame(
                StockChips.objects.filter(symbol=symbol)
                .values_list('date', variable)
            )

            daily_close = pd.DataFrame(
                StockPrice.objects.filter(symbol=symbol)
                .values_list('close')
            )
            data = pd.concat([data, daily_close], axis=1)

        data.columns = ['date', variable, 'close']
        LatestUpdate = list(data.date)[-1]
        LatestPrice = list(data.close)[-1]
        data.date = pd.to_datetime(data.date)

        data, script, div = bokeh_plotting(data, variable)
        data = data.round(2)
        data.index = data.index.strftime('%Y-%m')
        datatable = pd.DataFrame(data[variable])
        datatable.columns = [english_to_chinese(variable)]
        datatable.index.name = '月份'
        df2html = datatable.T.to_html()

        context = {
            'symbol': symbol,
            'script': script,
            'div': div,
            'datatable': df2html,
            'url': variable,
        }

        return JsonResponse(context, status=200)

    data = pd.DataFrame(
        StockPrice.objects.filter(symbol=symbol)
        .values_list('date', 'close')
    )
    data.columns = ['date', 'close']
    LatestUpdate = list(data.date)[-1]
    LatestPrice = list(data.close)[-1]

    BasicInfo = StockBasic.objects.get(symbol=symbol)
    context = {
        # 'script': script,
        # 'div':div,
        # 'datatable':df2html,
        'symbol': symbol,
        'name': BasicInfo.name,
        'industry': BasicInfo.industry,
        'list_date': BasicInfo.listed_date,
        'latestprice': LatestPrice,
        'latestupdate': LatestUpdate,
    }

    return render(request, 'info/info.html', context)
