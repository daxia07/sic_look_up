from sic_look_up import init
import pandas as pd


def get_query_data():
    query = pd.read_excel('files/sic_look_up_list.xlsx', sheet_name='list')
    return query


def get_result(query, data):
    query.SIK = query.SIK.astype(str)
    res = query.merge(data, on='SIK', how='left')
    return res


def run():
    data = init()
    query = get_query_data()
    res = get_result(query, data)
    res.to_csv('files/res.csv', index=False)
    print(res)


if __name__ == '__main__':
    run()
