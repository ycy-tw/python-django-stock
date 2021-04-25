from django.test import TestCase
from info.models import StockBasic, StockChips, StockPrice
from .views import BasicConditions, ChipsConditions
import pandas as pd

# Create your tests here.
# class BasicConditionTest(TestCase):

#     def test_pe(self):

#         condition = {'pe':['小於', '8']}
#         priceTable = pd.DataFrame(StockPrice.objects.all().values())
#         qualifiedSymbols, firmAttrResult = BasicConditions(priceTable, condition)
#         self.assertEqual(qualifiedSymbols, {2474, 2881})

