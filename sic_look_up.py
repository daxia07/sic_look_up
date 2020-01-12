import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
import pandas as pd


def init(url='http://www.ehso.com/siccodes.php'):
    try:
        raw_table = fetch_table(url)
        res = format_table(raw_table)
        return res
    except Exception as e:
        print(e)
        print('Exception occurred, aborting!')


def fetch_table(url):
    try:
        response = requests.get(url)
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        res = soup.find_all('small')
        if len(res) == 1:
            return res[0]
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        print('Success!')


def format_table(raw_input):
    res = pd.DataFrame(columns=['SIK', 'name', '3', '2', 'DIV'])
    new_row = {'SIK': None, 'name': None, '3': None, 'DIV': None}
    for row in raw_input:
        # remove ending \n, leading white space, <br/>, then remove leading and trailing spaces
        entry = str(row).replace('\n', '').replace('\xa0', '').replace('<br/>', '').strip()
        if len(entry) == 0:
            # in this case <br/>
            continue
        # if DIVISION, fill in, otherwise fill in columns needed
        entry_tuple = entry.split(" ", 1)
        if len(entry_tuple) != 2:
            raise ValueError('entry_tuple length should be 2!', entry)
        indicator, val = entry_tuple
        if indicator == 'DIVISION':
            new_row['DIV'] = val
            new_row['2'] = None
            new_row['3'] = None
            new_row['SIK'] = None
            continue
        if not indicator.isdigit():
            raise ValueError('indicator not DIV or digit!', entry)
        if len(indicator) == 3:
            # add new entry
            new_row['SIK'] = indicator.ljust(4, '0')
            new_row['name'] = val
            new_row['3'] = None
            res = res.append(new_row, ignore_index=True)
            new_row['SIK'] = None
            new_row['name'] = None
            new_row['3'] = val

        elif len(indicator) == 2:
            new_row['SIK'] = indicator.ljust(4, '0')
            new_row['name'] = val
            new_row['2'] = None
            res = res.append(new_row, ignore_index=True)
            new_row['3'] = None
            new_row['SIK'] = None
            new_row['name'] = None
            new_row['2'] = val

        elif len(indicator) == 4:
            # to append
            new_row['SIK'] = indicator
            new_row['name'] = val
            res = res.append(new_row, ignore_index=True)
            new_row['SIK'] = None
    return res


if __name__ == '__main__':
    res = init()
    print(res)
