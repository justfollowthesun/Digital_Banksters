from .config import *
import requests





def gropus(kword, count, city_id, acess_token=access_token, version=version ):
    response = requests.get('https://api.vk.com/method/groups.search', params={
        'access_token': acess_token,
        'q': kword,
        'v': '5.131',
        'city_id': city_id,
        'count': count
    }).json()['response']['items']
    group_ids = [g['id'] for g in response]
    return group_ids


def list_gropus(keywords, count, city_id):
    group_list = []
    for kword in keywords:
        group_kword = gropus(kword, count,city_id)
        group_list = group_list + group_kword
    return group_list
