from config import *
import time
import requests
from test_data import *

days = 70

def times(days:int) -> int:
    '''
    Преобразует количетсво дней в секунды (unixtime)
    :param days: кол-во дней
    :return: интервал в секундах соотв. кол-ву дней days
    '''
    end_time = (int(time.time()))
    start_time = end_time - days*86400
    return (start_time, end_time)


def news_count(banksters_dict:dict, access_token:str, days:int) -> dict:
    start_time = times(days)
    '''
    Вычисляет нормированное количество новостей конкурентов
    :param banksters_dict: словарь где каждому названию банка соотв. url
    :param access_token: token для api-соединения (при истечение срока использования токена см. config.py
    :param start_time:  время в формате unixtime, начиная с которого происходит поиск записей
    :return: словарь с нормированной частотой упоминаний конкурирующих банков
    '''
    news = {}
    for bank in list(banksters_dict.keys()):
        bank_url = banksters_dict[bank]
        try:
            response = requests.get('https://api.vk.com/method/newsfeed.search', params={
                'access_token': access_token,
                'q': [f'{bank}',f'{bank_url}'],
                'start_from':start_time,
                'v': '5.131'
            }).json()['response']
        except:
            pass
        print(response)
        news[bank] = response['total_count']
    for bank in list(news.keys()):
        news[bank] = news[bank] / news['уралсиб']
    return news

print(news_count(banksters_dict, access_token,days ))




