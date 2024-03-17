# TIC-TAC-TOE


#### Подготовил:
> Шарапов Егор Сергеевич, БПИ219

## Дополнительная информация
#### [Коллекция на Postman](https://www.postman.com/mission-technologist-87573140/workspace/agents/collection/27605275-db3b9b2e-8bbd-4a1d-8dae-02b8b648af44?action=share&creator=27605275)

### Использованные технологии
- [**Flask**](https://flask.palletsprojects.com/en/2.3.x/)
- [**Python 3**](https://www.python.org/downloads/)
- [**Postman**](https://www.postman.com/)

## Библиотеки

- **sqlite3**
- **time**
- **flask**

## Структура проекта
> ### **game_client**
> Данный модуль - клиент игры.
>- client.py _(содержит все для игры в консоли)_


> ### **game_server**
> Данный модуль содержит набор вспомогательных функций.
> - app.py _(содержит все нужные конечные точки для работы игры)_

> ### **record_server**
> Данный модуль содержит набор вспомогательных функций.
> - app.py _(содержит все нужные конечные точки для работы таблицы лидеров)_

## ЗАПУСК
Создайте сеть в общей папке проекта:

```BASH
docker network create server_network
``` 

### **В отдельном терминале №1**

Перейдите в папку ``game_server``:

```BASH
cd ./game_server
```

Поднимите контейнер

```BASH
docker-compose up --build
```

### **В отдельном терминале №2**

Перейдите в папку ``record_server``:

```BASH
cd ./record_server
```

Поднимите контейнер

```BASH
docker-compose up --build
```

### **В отдельном терминале №3-N**

Перейдите в папку ``game_client``:

```BASH
cd ./game_client
```

Запускаем 

```BASH
python client.py
```

> Далее действуем по инструкциям, подключайтесь с разными id. 
> Автоматическая система мачмейкинга подберет лобби каждому из клиентов.