import requests
from bs4 import BeautifulSoup
import datetime
import time

def parse_news(resource_id, resource_name, resource_url, top_tag, bottom_tag, title_cut, date_cut):
    # Распаковка структур(списков) из таблицы resources:
    
    # Список стуктуры параметра resource_url
    resource_url_args = resource_url.split(', ')

    # Список стуктуры параметра top_tag
    top_tag_args = top_tag.split(', ')

    # Список стуктуры параметра bottom_tag
    bottom_tag_args = bottom_tag.split(', ')

    # Список стуктуры параметра title_cut
    title_cut_args = title_cut.split(', ')

    # Список стуктуры параметра date_cut
    date_cut_args = date_cut.split(', ')

    # Уровень новостного меню (счётчик)
    level_count = int(resource_url_args[2])

    # Переменная для сравнения со счётчиком
    count = level_count - 1

    # Базовая ссылка на новостное меню
    news_menu_url = resource_url_args[0] + resource_name + resource_url_args[1]

    # Выходной список, формирующий таблицу items
    news = []

    while level_count > 0: # Для получения ссылок второго уровня
        # Получение запроса на получение меню новостей второго (следующего) уровня (для сайта с пагинацией страниц)
        if level_count == count:
            response = requests.get(news_menu_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                paginator_a_tags = soup.find(top_tag_args[6], class_=top_tag_args[7])
                paginator_a_tag = paginator_a_tags.find(bottom_tag_args[6], class_=bottom_tag_args[7])
                news_menu_url = resource_url_args[0] + resource_name + paginator_a_tag['href']

        # Получение запроса на получение меню новостей
        response = requests.get(news_menu_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            div_tags = soup.find_all(top_tag_args[0], class_=top_tag_args[1])

            # Получение ссылок текущего уровня
            a_hrefs = []
            for div_tag in div_tags:
                a_tags = div_tag.find_all(bottom_tag_args[0], class_=bottom_tag_args[1])
                # Получение ссылок и проверка их на полноту перед добавлением в список a_hrefs
                for a_tag in a_tags:
                    if (resource_url_args[0] + resource_name) not in a_tag['href']:
                        a_href = resource_url_args[0] + resource_name + a_tag['href']
                        a_hrefs.append(a_href)
                    else:
                        a_hrefs.append(a_tag['href'])

            # Получение запроса на получение ссылок на новости
            for i in range(len(a_hrefs)):
                response = requests.get(a_hrefs[i])
                if response.status_code == 200:
                    # Используем BeautifulSoup для парсинга HTML-контента
                    soup = BeautifulSoup(response.content, 'html.parser')
                    title = soup.find(title_cut_args[1], class_=title_cut_args[0]).text.strip()

                    # Получение даты и времени со страницы с новостью
                    newsdate = soup.find(date_cut_args[0], class_=date_cut_args[1])
                    news_datetime_str = newsdate.get('datetime')

                    # Получение содержимого со страницы с новостью
                    content = soup.find(top_tag_args[2], class_=top_tag_args[3]).text.strip()

                    # Получение даты и времени со страницы с новостью в формате Unix time
                    datetime_obj = datetime.datetime.strptime(news_datetime_str, date_cut_args[2])
                    nd_date = int(datetime_obj.timestamp())

                    # Получение даты со страницы с новостью в формате Год-Месяц-День
                    datetime_obj = datetime.datetime.strptime(news_datetime_str, date_cut_args[2])
                    not_date = datetime_obj.strftime('%Y-%m-%d')

                    # Формируем выходной список функции parse_news()
                    news.append(resource_id)
                    news.append(a_hrefs[i])
                    news.append(title)
                    news.append(content)
                    # news.append(news_datetime_str)
                    news.append(nd_date)
                    news.append(not_date)

            level_count -= 1

    return news
