# Репозиторий команды Digital Banksters на Moscow City Hack 2022

<a href="https://ibb.co/jwDMSgR"><img src="https://i.ibb.co/GMR2qcT/photo-2022-06-13-01-36-29.jpg" alt="photo-2022-06-13-01-36-29" border="0"></a>
# 0. Структура репозитория
Весь код для парсинга содержится в `parsing`, в котором имеется три подкаталога:
`vk` - парсинг vk.com
`telegram` - парсинг телеграм-каналов
`nlp_models` - код и модели для NLP с помощью методов глубокого обучения

# 1 Рекомендации относительно рекламы продукта в сообществах vk и telegram-каналах.
## 1.1 Входные данные
Пользователь вводит адрес интересующего сообщества, например:
`https://vk.com/optar` 
`https://t.me/banksta`
`n` - число новостей для парсинга
В качестве описания ЦА каждого продукта на вход подается список ключевых слов, например:

`products = {
    'Дебетовые карты': ['путешествия', 'инвестиции', 'улучшение условий труда'],
    'Кредитные карты': ['комфорт', 'удовольствие', 'гламур', 'технологии'],
    'Продукты для ЮЛ': ['путешествия', 'накопление сбережений', 'автомобиль', 'образование', 'финансы', 'инвестиции'],
    'Кредит' : ['деньги', 'успех', 'роскошь']
}`

## 1.2 Описание базовой технологии

В качестве меры семантической близости междду ключевым словом и текстом была выбрана **cosine similarity**, вычисляемая по следующей формуле:

<a href="https://imgbb.com/"><img src="https://i.ibb.co/4pJn0kp/download.png" alt="download" border="0"></a>

где **А** - вектор, полученный из ключевого слова,
**В** - вектор, полученный из текста новости.

Значения cosine similarity составляют:

1 - Для полностью идентичных по смыслу слов (cos0)
-1 - Для полностью противоположных (cos180)

Векторизация текста осуществлялась с помощью библиотеки `spacy` и модели **ru_core_news_md-3.3.0** [1]с параметрами точности токенизации:
$$ Fscore=0.98 $$
$$ Rscore=0.98 $$

Оценка с помощью итерирации по ключевым словам для данной категории продукта,суммирования  и нормирования cosine similarity по всем `n` новостям.  Полученное значение возвращается в качестве количественной оценки целесообразности рекламы продукта в данном сообществе, в зависимости от этого представляются рекомендации по рекламе:

**Дебетовые карты** -  Предлагать

**Кредитные карты** - Подумать

**Продукты для ЮЛ** - Не предлагать

**Кредит** - Прелагать

# 2 Поиск упоминаний банковских продуктов конкурентов
## 2.1 Входные данные
В пользовательском интерфейсе задается список конкурентов (для тестирования были выбраны):
1) Тинькофф
2) ВТБ
3) Газпромбанк
4) Альфа-банк
5) Россельхозбанк
6) Открытие
7) Совкомбанк
8) Райффайзенбанк
9) Росбанк
10) Уралсиб
Поиск осуществляется по ссылке на группу в vk или телеграм-канал:
`https://vk.com/optar` 
`https://t.me/banksta`
Задается количество новостей, за которые необходимо проведение поиска (в дальнейшей разработке можно заменить на промежуток дат):
`n` - число новостей для парсинга
## 2.1 Описание базовой технологии
Данная задача представляет собой поиск именованных сущностей в рамках обработки естественного языка, который осуществлялася с помощью модели глубокого обучения **SlovNet: slovnet_ner_news_v1 ** [2] проекта **Natasha** [3]. Критериями  выбора  являлись показатели качества, скорости работы и удобство деплоя на сервер. Метрики качества Named-Entity-Recognition, полученные на датасете `factru` [2] (наряду с `slovnet_bert` и `deeppavlov_bert` входит в топ-3 моделей):
$$ PER=0.959 $$
$$ LOC=0.915 $$
$$ ORG=0.825 $$

Из текста новости выделяются именованные сущности:
```
Уралсиб Бонус: отвечаем на частые вопросы
ORG──────────                            
Хотите получать кешбэк до 3 % и пользоваться услугами для путешествий?
С программой Уралсиб Бонус накопленные бонусные рубли приносят 
             ORG──────────                                     
реальную пользу 😎 
Отвечаем на часто задаваемые вопросы: 
💸 За какие операции начисляются бонусные рубли? 
Бонусные рубли начисляются за покупки по карте или покупки с 
использованием реквизитов карты в интернете. 
Не начисляются за операции с наличными через банкоматы, переводы на 
карты и счета, оплату налогов и штрафов, страховых премий и взносов, 
платежей ЖКХ и расходы на азартные игры. 
💸 По какому курсу начисляются бонусные рубли? 
Бонусные рубли начисляются в виде процента от общей суммы трат за 
месяц по курсу 1 бонусный рубль = 1 рубль РФ. 
                                          LOС  
💸 На какой счёт будет зачислен кешбэк? 
Кешбэк зачисляется на счёт действующей рублёвой карты, которая 
последней была подключена к программе. 
 
💸 Как стать участником программы лояльности Уралсиб Бонус? 
                                            ORG──────────  
Если у вас есть дебетовая карта «Прибыль» или «Кредитная карта с 
кешбэком», программа подключена автоматически. В остальных случаях вас
 может проконсультировать наш специалист.
Узнайте больше о программе лояльности Уралсиб Бонус (https://bonus.ura
                                      ORG──────────                   
lsib.ru/utm_source=telegram.com&utm_medium=post&utm_campaign=bonus?utm
_term=otvechaemnavoprosy)
```
ORG - Организация
LOC - Локация 

Найденные сущности фильтруются по параметру ORG. Схожесть каждой сущности с названием банка из п. 2.1 оценивается по следующему алгоритму:

0.  Строка содержащая сущность и название банка приводятся к нижнему регистру и удаляется подстрока 'банк':

`"Уралсиб Бонус"->"уралсиб бонус"`
`"Уралсиб"->"уралсиб"`

1.  Вычисляется длина пересечения множеств букв названия сущности и строки из п.0:

`len(("у","р","а","л","с","и","б")&("у","р","а","л","с","и","б"," ","б","о","н","у","с")) = len(["р", "а", "л", "и", "с", "у", "б"])=7`

3.  Полученное значение делится на длину названия банка:

`len(('у','р','а','л','с','и','б') / 7 = 1`

Число, полученное в п.3 служит количественным критерием похожести названий. В разработке сервиса пороговое значение было принято равным 0.8 
 
 # 3 Нейросеть для пределения наиболее релевантных признаков для банковского продукта
 
 
 # 4 Возможность автоматического поиска и выгрузки по заданному запросу и городу vk
 По заданному запросу, который содержит ключевые слова для поиска и города, происходит выгрузка сообществ, удовлетворяющих заданным параметрам. Формируется список пользователей, в котором каждый пользователь уникален. Предложение продуктов банка происходит с помощью данных о ЦА, собираемых банком и согласно критериям из п.3. Из полученного пула считываем характеристики и  выделяем пользователей каждого конкретного кредитного продукта. Получаемые параметры пользователей:
1. Дата рождения
2. Пол
3. Страна проживания
4. Город 
5. Образование


 # 4 Мониторинг упоминания конкурентов в новостях vk
Поиск упоминаний брендов конкурентов (упоминание должно содержать название конкурента и ссылку на его сайт). Выгрузка упоминаний брендов происходит на `n` дней (задается пользователем). Организации для сравнения так же задаются пользователем, полученная статистика нормируется на число упоминаний самого банка. Пример поиска относительной частоты упоминаний бренда за 30 дней:

**Уралсиб**: 1.0

**Тинькофф**: 308

**Cбер**: 15

**Втб**: 9

**Газпромбанк**: 0.002

**Альфа-банк**: 50

**Россельхозбанк**: 2

**Банк открытие**: 177
**Совкомбанк**: 1

**Райффайзенбанк**: 2

**Росбанк**: 1



# 5 Ссылки
1. Описание модели ru_core_news_md-3.3.0. Содержит количественные оценки точности работы и схему классификации https://spacy.io/models/ru
2. SlovNet - модель глубокого обучения для работы с ркусскоязычными текстами https://github.com/natasha/slovnet
3. Natasha - библиотека для решения NLP задач для русского языка
https://github.com/natasha
