from .models import Resource, Items

# nur.kz
# resource_name = 'nur.kz'
# resource_url = 'https://www., /latest, 1'
# top_tag = 'div, block-infinite js-infinite, div, formatted-body__content--wrapper'
# bottom_tag = 'a, article-preview-category__content, h2, formatted-body__header2, p, align-left formatted-body__paragraph' \
#              ' p, align-left formatted-body__paragraph'
# title_cut = 'h1, main-headline js-main-headline'
# date_cut = 'time, datetime datetime--publication, %Y-%m-%dT%H:%M:%S%z'


# scientificrussia.ru
# resource_name = 'scientificrussia.ru'
# resource_url = 'https://www., /news, 2'
# top_tag = 'div, image, div, article-text, , , li, page-item prev'
# bottom_tag = 'a, , h2, , p, , a, page-link'
# title_cut = 'h1, '
# date_cut = 'time, , %Y-%m-%d %H:%M'


# Импортируем функции рендеринга, перенапрвления и получения объекта модели из пакета функций быстрого доступа
from django.shortcuts import render, redirect, get_object_or_404

# Импортируем функцию parse_news()
from .parsefunc import parse_news

# Обработчик ввода/вывода
def getparsing(request):
    # Обрабатываем форму
    if request.method == 'POST':
        sitename = request.POST.get('parsesite')
        resourceset = Resource.objects.filter(resource_name=sitename)
        resourcesetlst = resourceset.values()

        # Проверяем совпадение введенного названия с имеющимся в таблице resources БД
        for item in resourcesetlst:
            resource_name = item['resource_name']
            resource_id = item['resource_id']
            break

        # Получение названия из таблицы resources в БД
        if sitename == resource_name:
            for item in resourcesetlst:
                resource_name = item['resource_name']
                resource_id = item['resource_id']
                resource_url = item['resource_url']
                top_tag = item['top_tag']
                bottom_tag = item['bottom_tag']
                title_cut = item['title_cut']
                date_cut = item['date_cut']
                break

            # Активация функции parse_news (запуск парсера)
            news = parse_news(resource_name, resource_url, top_tag, bottom_tag, title_cut, date_cut)
            resourceset = Resource.objects.all()
            resourcesetlst = resourceset.values()

            # Повторное сохранения значения id ресурса в переменной
            for item in resourcesetlst:
                resource_id = item['resource_id']
                break

            # Импорт пакета для получения даты записи данных в таблицу items
            from datetime import datetime
            current_datetime = datetime.now()

            # Формирование переменных (для наглядности) для записи в таблицу items БД
            for i in range(0, len(news), 6):
                res_id = resource_id
                link = news[i]
                title = news[i + 1]
                content = news[i + 2]
                nd_date = news[i + 4]
                not_date = news[i + 5]
                s_date = int(current_datetime.timestamp()) # в формате UnixTime

                # Получение объекта с добавленные в ORM-модель Items данными
                news_item_obj = Items.objects.create(res_id=res_id, link=link, title=title, content=content,
                                                     nd_date=nd_date, s_date=s_date, not_date=not_date)

                # Сохранение объекта модели
                news_item_obj.save()

            # Получение QuerySet, отфильтрованного по id из таблицы items
            itemsset = Items.objects.filter(res_id=res_id)

            # Получение QuerySet, отфильтрованного по id из таблицы resources
            resourceset = Resource.objects.get(resource_name=sitename)

            # Прерывистая линия
            multydash = '-'*125

            # Сообщение об окончании парсинга
            endparse = 'Парсинг окончен!'

            # Добавление переменных в словарь контекста для рендеринга
            context = {'endparse': endparse, 'resourceset': resourceset, 'itemsset': itemsset, 'multydash': multydash}

            # Рендеринг шаблона
            return render(request, 'parsersystem/parsing.html', context)
        else:
            # Сообщение об ошибке ввода
            endparse = 'Название введено неверно!!'
            context = {'endparse': endparse}
            return render(request, 'parsersystem/parsing.html', context)
    else:
        # Если запрос по какой-то причине был не POST (GET)
        return render(request, 'parsersystem/parsing.html')