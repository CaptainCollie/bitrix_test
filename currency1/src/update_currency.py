from config import webhook
from fast_bitrix24 import Bitrix
from get_currency import get_cbr_currency


def add_currency(b, country_code, amount_cnt=1):
    res = b.get_all('crm.currency.list')
    sort = 100
    if res:
        sort = int(res[-1].get('SORT')) + 100
    base_country = [i for i in res if i.get('BASE') == 'Y'][0].get('CURRENCY')
    amount = get_cbr_currency(base_country, country_code)
    print(base_country)
    if base_country == 'RUB':
        amount = get_cbr_currency(country_code)

    items = {
        'fields': {
            'CURRENCY': country_code,
            'AMOUNT_CNT': amount_cnt,
            'AMOUNT': amount * amount_cnt,
            'SORT': sort,
        }
    }

    b.call('crm.currency.add', items)


def update_currency(b, id=None, amount_cnt=1):
    res = b.get_all('crm.currency.list')
    base_country = [i for i in res if i.get('BASE') == 'Y'][0].get('CURRENCY')
    if id:
        amount = get_cbr_currency(base_country, id)
        sort = [i for i in res if i.get('CURRENCY') == id][0].get('SORT')
        items = {
            'id': id,
            'fields': {
                'AMOUNT_CNT': amount_cnt,
                'AMOUNT': amount,
                'SORT': sort,
            }
        }
        b.call('crm.currency.update', items)
    else:
        for i in res:
            id = i.get('CURRENCY')

            if id == 'RUB':
                amount = get_cbr_currency(base_country)
            elif id == base_country:
                amount = 1.0000
            else:
                amount = get_cbr_currency(base_country, id)

            sort = [i for i in res if i.get('CURRENCY') == id][0].get('SORT')
            items = {
                'id': id,
                'fields': {
                    'AMOUNT_CNT': amount_cnt,
                    'AMOUNT': amount,
                    'SORT': sort,
                }
            }
            b.call('crm.currency.update', items)


def start():
    b = Bitrix(webhook)
    update_currency(b)