import requests
import fake_useragent
import json
from bs4 import BeautifulSoup


def get_cbr_currency(cntr_code_fst, cntr_code_snd=None):
    """
    Функция для получения курса валют с сайта Центробанка. Принимает строку с цифровым или буквенным кодом страны.
    Возвращает курс валюты.
    :param cntr_code_fst: str
    :param cntr_code_snd: str
    :return: float
    """

    user = fake_useragent.UserAgent().random

    header = {"user-agent": user}

    link = "https://www.cbr.ru/currency_base/daily/"
    response = requests.get(link, headers=header).text
    soup = BeautifulSoup(response, "lxml")

    table = soup.find('div', class_='table')
    all_cntrs = table.find_all('tr')
    dic_all_cntrs_ltr_code = {
        i.find_all('td')[1].text: float(i.find_all('td')[4].text.replace(',', '.')) / int(i.find_all('td')[2].text)
        for i in all_cntrs if i.find_all('td')}  # Словарь с буквенным кодом страны в виде {'AUD': 53.9975}
    dic_all_cntrs_digit_code = {
        i.find_all('td')[0].text: float(i.find_all('td')[4].text.replace(',', '.')) / int(i.find_all('td')[2].text)
        for i in all_cntrs if i.find_all('td')}  # Словарь с цифровым кодом страны {'036': 53.9975}

    cntr_code_fst = cntr_code_fst.upper()
    cntr_code_snd = cntr_code_snd.upper() if cntr_code_snd else cntr_code_snd

    if not (dic_all_cntrs_digit_code.get(cntr_code_fst) or dic_all_cntrs_ltr_code.get(
            cntr_code_fst)):
        return f'There is no {cntr_code_fst} in list'

    if cntr_code_snd and cntr_code_fst != cntr_code_snd:
        return round(dic_all_cntrs_digit_code.get(cntr_code_fst) / dic_all_cntrs_digit_code.get(
            cntr_code_snd), 4) if dic_all_cntrs_digit_code.get(cntr_code_snd) else round(dic_all_cntrs_ltr_code.get(
            cntr_code_fst) / dic_all_cntrs_ltr_code.get(cntr_code_snd), 4)
    else:
        return dic_all_cntrs_digit_code.get(cntr_code_fst) if dic_all_cntrs_digit_code.get(
            cntr_code_fst) else dic_all_cntrs_ltr_code.get(cntr_code_fst)
