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



def name2id(group_name):

    response = requests.get('https://api.vk.com/method/utils.resolveScreenName', params={
        'access_token': access_token,
        'screen_name':group_name,
        'v': 5.103,
    }).json()['response']
    return response['object_id']

def wall_news(id, news_num):
    response = requests.get('https://api.vk.com/method/wall.get', params={
        'access_token': access_token,
        'owner_id': -1*id,
        'v': 5.103,
        'count': news_num,
    }).json()['response']['items']
    return response


def product_scores(news_list, products=products):
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


def product_recommendations(url, news_num):
    group_name = url.split('vk.com/')[-1]
    id = name2id(group_name)
    print(id)
    news_list = wall_news(id, news_num)
    scores = product_scores(news_list)
    print(scores)



product_recommendations('https://vk.com/optar', 10000)



