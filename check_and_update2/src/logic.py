from src.config import webhook
from fast_bitrix24 import Bitrix
import json

deal_fields_dic = {
    'description': 'UF_CRM_1628719052',
    'products': 'UF_CRM_1628719186',
    'delivery_address': 'UF_CRM_1628719194',
    'delivery_date': 'UF_CRM_1629038807',
    'delivery_code': 'UF_CRM_1628719217',
}

contact_fields_dic = {
    'phone': 'UF_CRM_1628715752',
    'address': 'UF_CRM_1628715760'
}


def add_contact(b, contact: dict):
    """
    Функция для добавления контакта
    :param b: Bitrix
    :param contact: dict
    :return: None
    """
    contact.setdefault('NAME', contact.get('name'))
    contact.setdefault('LAST_NAME', contact.get('surname'))
    contact = {contact_fields_dic[i] if i in contact_fields_dic else i: j for i, j in contact.items() if
               i not in ('name', 'surname')}
    b.call('crm.contact.add', {'fields': contact})


def add_deal(b, deal: dict):
    """
    Функция для добавления сделки
    :param b: Bitrix
    :param deal: dict
    :return: None
    """
    deal.setdefault('CONTACT_ID', get_contact_id(b, deal.get('client')))
    b.call('crm.deal.add', {'fields': deal})


def check_deal(b, deal: dict):
    """
    Функция проверяет существует ли сделка, если нет - добавляет, если да - обновляет
    :param b: Bitrix
    :param deal: dict
    :return: None
    """
    deals = get_deals(b)
    check_and_add_contact(b, deal.get('client'))
    check = 0
    for i in deals:
        if i.get('TITLE') == deal.get('TITLE') or i.get(deal_fields_dic.get('delivery_code')) == deal.get(
                deal_fields_dic.get('delivery_code')):
            id = i.get('ID')
            check = 1
            break
    if check:
        update_deal(b, id, deal)
    else:
        add_deal(b, deal)


def check_and_add_contact(b, contact: dict):
    """
    Функция проверяет существует ли контакт, если нет - добавляет
    :param b: Bitrix
    :param contact: dict
    :return: None
    """
    contacts = b.get_all('crm.contact.list', {
        'select': ['NAME', 'LAST_NAME', 'UF_*']
    })
    check = 0
    for cont in contacts:
        cont_tmp = {i: j for i, j in cont.items() if i != 'ID'}
        if set(cont_tmp.values()) == set(contact.values()):
            id = cont['ID']
            check = 1
    if not check:
        add_contact(b, contact)


def get_contact_id(b, contact: dict):
    """
    Функция получает id контакта
    :param b: Bitrix
    :param contact: dict
    :return: int
    """
    contacts = b.get_all('crm.contact.list', {
        'select': ['NAME', 'LAST_NAME', 'UF_*']
    })
    id = 0
    for cont in contacts:
        cont_tmp = {i: j for i, j in cont.items() if i != 'ID'}
        if set(cont_tmp.values()) == set(contact.values()):
            id = cont['ID']
            break
    if id:
        return id


def get_deals(b):
    """
    Функция для получения списка сделок
    :param b: Bitrix
    :return: list
    """
    return b.get_all('crm.deal.list', {
        'select': ['TITLE', 'UF_*', 'CONTACT_ID']
    })


def get_deals_from_json(file):
    """
    Функция для чтения JSON файла и получения списка сделок
    :param file: str
    :return: list
    """
    with open(file, 'r') as f:
        items = json.load(f)
        for i in range(len(items)):
            items[i]['TITLE'] = items[i].get('title')
            items[i] = {i: ', '.join(j) if i == 'products' else j for i, j in items[i].items()}
            items[i] = {deal_fields_dic[i] if i in deal_fields_dic else i: j for i, j in items[i].items() if
                        i != 'title'}
    return items


def update_deal(b, id: int, deal: dict):
    """
    Функция для обновления сделки
    :param b: Bitrix
    :param id: int
    :param deal: dict
    :return: None
    """
    b.call('crm.deal.update', {
        'id': id,
        'fields': deal
    })


def start(file):
    b = Bitrix(webhook)
    deals = get_deals_from_json(file)
    for deal in deals:
        check_deal(b, deal)
