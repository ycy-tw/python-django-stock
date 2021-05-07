import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('sqlite:///db.sqlite3')

for csvfile, model in [
    ('demodata/stockbasic.csv', 'info_stockbasic'),
    ('demodata/stockchips.csv', 'info_stockchips'),
    ('demodata/stockprice.csv', 'info_stockprice'),
]:

    df = pd.read_csv(csvfile, index_col=False)
    df.to_sql(
        name=model,
        con=engine,
        if_exists='append',
        index=False,
    )

    print(csvfile + ', Successfully Insert.')

# python demodata/addDemoData.py
