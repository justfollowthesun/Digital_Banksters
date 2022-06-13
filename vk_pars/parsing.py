from vk_pars.config import *
import requests

# При возникновении ошибки KeyError вам нужно зайти в config и получить новый access token согласно инструкциям в файле

def gropus(kword: str, count: int, city_id:int, acess_token=access_token) -> list:
    '''
    Возвращает список идентификаторов групп, соотв. заданному городу
    :param kword: ключевое слово для поиска
    :param count: количество групп для выдачи по каждому ключевому слову
    :param city_id: идентификатор города
    :param acess_token: токен для доступа через API
    :return: список id групп, соотв. запросу
    '''
    response = requests.get('https://api.vk.com/method/groups.search', params={
        'access_token': acess_token,
        'q': kword,
        'v': '5.131',
        'city_id': city_id,
        'count': count
    }).json()['response']['items']
    group_ids = [g['id'] for g in response]
    return group_ids


def list_gropus(keywords:list, count: int, city_id: int) -> list:
    '''
    Возвращает список id групп, соотв. заданным ключевым словам
    :param keywords: список ключевых слов
    :param count: число групп для поиска по каждому слову
    :param city_id: идентификатор города
    :return: список групп, соотв. запросу
    '''
    group_list = []
    for kword in keywords:
        group_kword = gropus(kword, count,city_id)
        group_list = group_list + group_kword
    return group_list

def get_users(group_id: int) -> dict:
    '''
    Получение профилей пользователей данной группы
    :param group_id:
    :return: список профилей из  групп
    '''
    user_profiles= {}
    try:
        response = requests.get('https://api.vk.com/method/groups.getMembers',params={
        'access_token': 'vk1.a.e9BEemTZ_M-bYs_lFDmJ9XU5-KVkP2sQNhXBDeevFJDk-RK9DKrFkXmMfqR6c-naJK3X-mN3k3pDBokuyDF9WxO_DJJBYrgJnGDCDryrl4O3YPKoM2LqTzC6I_dwxkLMXvYXyuF5t5yJomJT17_xp4TmqYgNJzDlicc3xMdkT2j5k214hsrJdaS33jXrn4WJ',
        'v': 5.103,
        'group_id': group_id,
        'sort': 'id_desc',
        'fields': ['bdate','country','city','education','sex','universities']}).json()['response']['items']
        for usr in response:
            user_profiles[usr['id']] =  [usr['bdate'], usr['country'], usr['city'], usr['education'], usr['sex']]
    except:
        pass
    return user_profiles

