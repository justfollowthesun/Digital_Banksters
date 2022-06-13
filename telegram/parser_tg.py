
from telegram.parsing_functions import *
from nlp_models import nlp_functions

'''
Can be improved using
https://betterprogramming.pub/extract-keywords-using-spacy-in-python-4a8415478fbf
pip install git+https://github.com/aatimofeev/spacy_russian_tokenizer.git

'''


products = {
    'Дебетовые карты': ['путешествия', 'инвестиции', 'улучшение условий труда'],
    'Кредитные карты': ['комфорт', 'удовольствие', 'гламур', 'технологии'],
    'Продукты для ЮЛ': ['путешествия', 'накопление сбережений', 'автомобиль', 'образование', 'финансы', 'инвестиции'],
    'Кредит' : ['деньги', 'успех', 'роскошь']
}


async def product_recomendations(products: list, url: str) -> dict:
    '''
    :param products:
    Список продуктов банка, по которым происходит поиск
    :param url:
    :return
    '''
	# url = 'https://t.me/banksta'
    messages_num = 10
    channel = await client.get_entity(url)
    all_messages = await dump_all_messages(channel, messages_num)
    product_scores = {}
    for product in list(products.keys()):
        for category in products[product]:
            category_score = 0
            for msg in all_messages:
                msg_txt = msg['message']
                similarity = nlp_functions.cosine(category, msg_txt)
                category_score +=similarity
            category_score = category_score / len(all_messages)
        product_score = category_score / len(products)
        product_scores[product] = product_score
    print(product_scores)
    return product_scores


async def competitors_ner(url):
    reminders = {
        'Тинькофф': [0, []],
        'СберБанк': [0, []],
        'Втб': [0, []],
        'Газпромбанк': [0, []],
        'Альфа-банк': [0, []],
        'Россельхозбанк': [0, []],
        'Открытие': [0, []],
        'Совкомбанк': [0, []],
        'Райффайзенбанк': [0, []],
        'Росбанк': [0, []],
        'Уралсиб': [0, []]
    }

    channel = await client.get_entity(url)
    messages_num = 1000
    all_messages = await dump_all_messages(channel, messages_num)
    for msg in all_messages:
        try:
            message = msg['message']
            markup = nlp_functions.ner(message)
            spans = markup.spans
            spans = nlp_functions.spans_set(spans, message)
            for bank in list(reminders.keys()):
                count = 0
                for span in spans:
                    if nlp_functions.bank_similarity(bank, span) > 0.8:
                        count = count + 1
                        reminders[bank][0] += 1
                        # reminders[bank][1].append(message)
        except:
            pass
    print(reminders)
    return reminders


url = 'https://t.me/banksta'

with client:
	client.loop.run_until_complete(competitors_ner(url))

