from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from info.models import StockPrice, StockChips, StockBasic
from django.contrib.auth.decorators import login_required

import pandas as pd
import json
import csv
import codecs

PirceColumns = [
    'pe', 'pb', 'yield_rate',
]

ChipsColumns = [
    'margin_purchase', 'short_sale', 'foreign',
    'trust', 'dealer', 'ftd_total',
]


def GetSymbolsNames(symbols):
    names = dict(StockBasic.objects.filter(symbol__in=symbols).values_list('symbol', 'name'))
    return {'證券名稱':names}

def ColumnsNameToVariable(variable):

    ColumnToChinese = {
        'pe':'本益比',
        'pb':'股價淨值比',
        'yield_rate':'現金殖利率(%)',
        'margin_purchase':'融資',
        'short_sale':'融券',
        'foreign':'外資',
        'trust':'投信',
        'dealer':'自營',
        'ftd_total':'三大法人',
    }

    return ColumnToChinese[variable]


# Create your views here.
def VariableToColumnsName(variable):

    ChineseToColumn = {
        '本益比':'pe',
        '股價淨值比':'pb',
        '現金殖利率':'yield_rate',
        '融資':'margin_purchase',
        '融券':'short_sale',
        '外資':'foreign',
        '投信':'trust',
        '自營':'dealer',
        '三大法人':'ftd_total',
    }

    return ChineseToColumn[variable]


def ChipsConditions(df, oneCondition):

    firmAttr = list(oneCondition.keys())[0]
    moreOrLess, threshold = oneCondition[firmAttr]

    df = df[['date', 'symbol', firmAttr]]
    df.date = pd.to_datetime(df.date)
    df = df.set_index(['date', 'symbol']).unstack()
    df.columns = df.columns.droplevel()
    df = df.groupby(pd.Grouper(level='date',freq='M')).sum().iloc[-int(threshold):,:]

    qualifiedSymbols = set(df.columns[(df > 0).all() == True]) if moreOrLess in ['大於', '增加', '買超'] \
                                                               else set(df.columns[(df < 0).all() == True])

    qualifiedSymbolsValue = df[qualifiedSymbols].sum().to_dict()
    firmAttrResult = {f'{ColumnsNameToVariable(firmAttr)}近{threshold}個月累積(張)' : qualifiedSymbolsValue}

    return qualifiedSymbols, firmAttrResult


def BasicConditions(df, oneCondition):

    firmAttr = list(oneCondition.keys())[0]
    moreOrLess, threshold = oneCondition[firmAttr]
    lastestDate = df.date.max()
    df = df[df.date == lastestDate][['symbol', firmAttr]]
    df.set_index('symbol', inplace=True)

    if moreOrLess == '大於':
        qualifiedSymbols = set(df[ (df[firmAttr] >= float(threshold)) == True ].index)

    elif moreOrLess == '小於':
        qualifiedSymbols = set(df[ (df[firmAttr] < float(threshold)) == True ].index)

    qualifiedSymbolsValue = df[df.index.isin(list(qualifiedSymbols))][firmAttr].to_dict()
    firmAttrResult = {ColumnsNameToVariable(firmAttr) : qualifiedSymbolsValue}

    return qualifiedSymbols, firmAttrResult

def GetLatestStockReturn(symbols):

    df = pd.DataFrame(StockPrice.objects.all().values())
    df.date = pd.to_datetime(df.date)
    df = df[['date', 'symbol', 'close']]
    lastestDate = df.date.max()

    df = df.set_index(['date', 'symbol']).unstack()
    df.columns = df.columns.droplevel()
    df = df[df.index <= lastestDate][symbols]

    latestPrice = df.iloc[-1, :]
    lastTwentyPrice = df.iloc[-20, :]
    lastSixtyPrice = df.iloc[-60, :]
    lastHundredTwentyPrice = df.iloc[-120, :]

    latestPriceAndReturn =  {
                                f'最新收盤價':latestPrice.to_dict(),
                                '近20天報酬率(%)': ((lastTwentyPrice / latestPrice) - 1).to_dict(),
                                '近60天報酬率(%)': ((lastSixtyPrice / latestPrice) - 1).to_dict(),
                                '近120天報酬率(%)': ((lastHundredTwentyPrice / latestPrice) - 1).to_dict(),
                            }

    return latestPriceAndReturn

@login_required
def PickView(request):

    global filterResult

    if 'conditions' in request.GET:

        conditions = json.loads(request.GET.get('conditions'))

        for firmAttr in list(conditions.keys()):
            conditions[VariableToColumnsName(firmAttr)] = conditions.pop(firmAttr)

        finalQualifiedSymbols = set()
        finalOutputDict = {}
        firstAttr = True
        for firmAttr in conditions:

            callPriceTableYet = False
            callChipsTableYet = False

            if (firmAttr in PirceColumns):
                if callPriceTableYet == False:

                    priceTable = pd.DataFrame(StockPrice.objects.all().values())
                    callPriceTableYet = True
                    qualifiedSymbols, firmAttrResult = BasicConditions(priceTable, {firmAttr:conditions[firmAttr]})

                else:
                    qualifiedSymbols, firmAttrResult = BasicConditions(priceTable, {firmAttr:conditions[firmAttr]})

            elif (firmAttr in ChipsColumns):
                if callChipsTableYet == False:

                    chipsTable = pd.DataFrame(StockChips.objects.all().values())
                    callChipsTableYet = True
                    qualifiedSymbols, firmAttrResult = ChipsConditions(chipsTable, {firmAttr:conditions[firmAttr]})

                else:
                    qualifiedSymbols, firmAttrResult = ChipsConditions(chipsTable, {firmAttr:conditions[firmAttr]})

            # Once no result under one of the conditinos, means no qualified symbols.
            if (len(qualifiedSymbols) != 0):
                if (firstAttr == True):

                    finalQualifiedSymbols = qualifiedSymbols
                    finalOutputDict.update(firmAttrResult)

                else:

                    finalQualifiedSymbols = finalQualifiedSymbols & qualifiedSymbols
                    finalOutputDict.update(firmAttrResult)
            else:

                finalQualifiedSymbols = set()
                finalOutputDict = {}
                break

            firstAttr = False

        if len(finalQualifiedSymbols) != 0:

            latestPriceAndReturn = GetLatestStockReturn(finalQualifiedSymbols)
            symbolsAndNames = GetSymbolsNames(finalQualifiedSymbols)
            latestPriceAndReturn.update(finalOutputDict)
            symbolsAndNames.update(latestPriceAndReturn)

            filterResult = pd.DataFrame(symbolsAndNames).round(2)
            filterResult.index.name = '證券代號'
            filterResult = filterResult[filterResult.index.isin(finalQualifiedSymbols)]
            filterResult.reset_index(inplace=True)

            conditionResult = filterResult.T.to_dict()

        elif len(finalQualifiedSymbols) == 0:
            conditionResult = {}

        print('+----------------------+')
        print('|  Success Call Back!  |')
        print('+----------------------+')

        return JsonResponse({'conditionResult':conditionResult}, status=200)

    return render(request, 'pick/pick.html')


def DownloadPickResult(request):

    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    response.write(codecs.BOM_UTF8) # for chinese encoding problem

    try:
        writer.writerow(list(filterResult.columns))
        for i in range(len(filterResult)):
            writer.writerow(list(filterResult.loc[i].values))

        response['Content-Disposition'] = 'attachment; filename="result.csv"'

    except:
        response['Content-Disposition'] = 'attachment; filename="result.csv"'

    return response
