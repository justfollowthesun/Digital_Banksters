import vk
from nlp_models import nlp_functions
from vk_pars.parsing import *


session = vk.Session(access_token=access_token)
api = vk.API(session, v=v)

products = {
    'Дебетовые карты': ['путешествия', 'инвестиции', 'улучшение условий труда'],
    'Кредитные карты': ['комфорт', 'удовольствие', 'гламур', 'технологии'],
    'Продукты для ЮЛ': ['путешествия', 'накопление сбережений', 'автомобиль', 'образование', 'финансы', 'инвестиции'],
    'Кредит' : ['деньги', 'успех', 'роскошь']
}


# При возникновении ошибки KeyError вам нужно зайти в config и получить новый access token согласно инструкциям в файле



session = vk.Session(access_token=access_token)
api = vk.API(session, v=v)



def name2id(group_name: str) -> int:
    '''
    Преобразует имя группы из адресной строки в id
    :param group_name: преобразует короткое имя группы в id
    :return: id - уникальный идентификатор группы
    '''
    response = requests.get('https://api.vk.com/method/utils.resolveScreenName', params={
        'access_token': access_token,
        'screen_name':group_name,
        'v': 5.103,
    }).json()['response']
    return response['object_id']


def wall_news(id: int, news_num: int) -> dict:
    '''
    Получает список всех записей на стене сообщества по id
    :param id: id - уникальный идентификатор группы
    :param news_num: количество новостей
    :return: dict с записями из группы соотв. id
    '''
    response = requests.get('https://api.vk.com/method/wall.get', params={
        'access_token': access_token,
        'owner_id': -1*id,
        'v': 5.103,
        'count': news_num,
    }).json()['response']['items']
    return response


def product_scores(news_list: list, products: list) -> dict:
    '''
    Возвращает количественные оценки рекомендаций продуктов для рекламы
    :param news_list: список с новостями из заданной группы
    :param products: продукты банка
    :return:
    '''
    scores_dict = {}
    for product in list(products.keys()):
        for category in products[product]:
            category_score = 0
            for news in news_list:
                msg = news['text']
                similarity = nlp_functions.cosine(category, msg)
                category_score += similarity
            category_score = category_score / len(news_list)
        score = category_score / len(products)
        scores_dict[product] = score
    return scores_dict


def product_recommendations(url:str, news_num:int) -> dict:
    """
    Возвращает рекомендации продукта
    :param url: ссылка на канал в телеграме
    :param news_num: количество новостей для оценки
    :return: словарь с оценками
    """
    group_name = url.split('vk.com/')[-1]
    id = name2id(group_name)
    news_list = wall_news(id, news_num)
    scores = product_scores(news_list, products)
    return scores




