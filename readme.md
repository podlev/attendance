
# Электронный журнал
### Описание
Приложение для ведения электронного журнала и учета посещаемости студентов с графическим интерфейсом.

### Технологии
- Python
- PyQT
- CSV
- SQL

### Реализованные функции
- [x] Хранение данных в БД (Таблицы student, attendance, groups)
- [x] Создание и редактирование групп в приложении.
- [x] Создание и редактирование студентов в приложении.
- [x] Импорт студентов из CSV из приложения (пример Книга для импорта.csv).
- [x] Выставление посещаеомсти за конкретную дату.
- [x] Вывод общего списка посещамости по группе (Пример Программирование).

### Что надо добавить
- [ ] Экспорт журнала в CSV
- [ ] Заполнение посещаемости за все даты.
- [ ] Создание расписания
- [ ] Заполнение посещаемости с помощью RFID/NFC.

### Как запустить
1. Создать и активировать виртаульное окружение
 ```
python -m venv venv
source venv/Scripts/activate
```  
2. Установить зависимости
```
pip install -r requirements.txt
```
3. Запустить скрипт
```
python main.py
```

### Автор
Telegram: [Лев Подъельников](https://t.me/podlev)
