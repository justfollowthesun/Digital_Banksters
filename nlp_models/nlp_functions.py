import spacy
from slovnet import NER
from navec import Navec
from nlp_models.config import *

'''
https://github.com/natasha/slovnet#ner
https://github.com/natasha/natasha
'''


nlp = spacy.load(news_model_pth)
navec = Navec.load(navec_pth)
ner = NER.load(ner_pth)
ner.navec(navec)


banksters = {
    'Тинькофф': 'https://www.tinkoff.ru/',
    'Сбер': 'https://sber.ru/',
    'Втб': 'https://www.vtb.ru/',
    'Газпромбанк': 'https://www.gazprombank.ru/personal/page/online-bank',
    'Альфа-банк': 'https://alfabank.ru/',
    'Россельхозбанк': 'https://www.rshb.ru/',
    'Открытие': 'https://www.open.ru/',
    'Совкомбанк':'https://sovcombank.ru/',
    'Райффайзенбанк':'https://www.raiffeisen.ru/',
    'Росбанк':'https://www.rosbank.ru/',
    'Уралсиб': 'https://www.uralsib.ru/'
}

def spans_set(spans, text):
    spans_list= []
    for span in spans:
        if span.type =='ORG':
            start_pos = span.start
            stop_pos = span.stop
            word = text[start_pos:stop_pos]
            spans_list.append(word)
    spans = set(spans_list)
    return spans


def cosine(querry, text):
    querry_nlp =  nlp(querry)
    text_nlp = nlp(text)
    return querry_nlp.similarity(text_nlp)

def check_bank(word):
    word = word.replace('bank', '')
    word = word.replace('банк', '')
    return word


def bank_similarity(bank_name, bank_news):
    bank_name = bank_name.lower()
    bank_news = bank_news.lower()

    bank_name = bank_name.replace('банк', '')
    bank_news = bank_news.replace('банк', '')

    intersection_set= list(set(bank_name) & set(bank_news))

    intersection_value = len(intersection_set) / len(bank_name)
    return intersection_value

'''
Могут быть ошибки при упоминании продуктов конерктных банков без самих брендов. Например, данный подход пропустит следующий пост:

Продолжаем удивлять: сегодня мы снизили ставки по потребительским кредитам на один процентный пункт. А ещё запустили спецпредложение для подписчиков СберПрайм+

Теперь базовая ставка по кредиту на любые цели составляет 14,9% годовых. А в первый месяц — всего 8,9% годовых.

Для владельцев подписки СберПрайм+ же в первый месяц ставка и вовсе составит 6,9% годовых — при сумме кредита от 300 тысяч на год и более. Подобрать кредит под себя можно здесь (https://www.sberbank.ru/ru/person/credits/money/consumer_unsecured?).


'''

def banksters_ner(message):
    reminders = {
    'Тинькофф': [0, []],
    'СберБанк': [0,[]],
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

    markup = ner(message)
    spans = markup.spans
    spans = spans_set(spans, message)
    for bank in list(reminders.keys()):
        count = 0
        for span in spans:
            if bank_similarity(bank, span) > 0.8:
                count = count + 1

                reminders[bank][0] += 1
        # reminders[bank][1].append(message)

    return reminders
