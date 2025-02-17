# Weather Forecast Bot
## Telegram Bot
   tg : @weather_centraluniv_bot
## Основной функционал
- Получение прогноза погоды на основе данных из API AccuWeather.
- Поддержка нескольких городов в одном запросе.
- Визуализация данных о температуре в виде графиков.
- Предоставление дополнительной информации о влажности, скорости ветра и вероятности осадков.
- Обработка ошибок и возврат понятных сообщений в случае проблем с запросами.

## Установка
1. Клонируйте репозиторий проекта:
   ```bash
   git clone https://github.com/Viurty/bot_project1
   ```

2. Установите необходимые зависимости:
   ```bash
   pip install -r requirements.txt
   ```

3. Создайте файл `.env` в корневой директории и добавьте ваш API-ключ:
   ```env
   API_TOKEN = '7819574769:AAGMUIYwg5o0d8GpMg_fA1-SR50R2oN4-mU'
   ACCUWEATHER_API_KEY = 'spfT2R28NnnmtGlikbyhDGsr2MR8VJyk'
   ```

4. Убедитесь, что у вас установлена библиотека `kaleido` для сохранения графиков в виде изображений:
   ```bash
   pip install -U kaleido
   ```

## Запуск приложения
1. Запустите Flask-приложение:
   ```bash
   python app.py #облегченная версия вебсайта из проекта 3
   ```
2. Приложение будет доступно по адресу: `http://127.0.0.1:5000`

3.Запустите Телеграм бота:
```bash
python bot.py
```


#### Возможные ошибки:
- Если сервер AccuWeather недоступен:
  ```json
  {
    "error": "Проблема с подключением к серверу AccuWeather."
  }
  ```
- Если название города введено неправильно:
  ```json
  {
    "error": "Ошибка обработки города. Проверьте название."
  }
  ```

## Основные команды и возможности
- Запрос прогноза на день для одного или нескольких городов.
- Вывод графиков температуры для выбранного города.
- Сообщения с дополнительными данными, такими как влажность, вероятность осадков и скорость ветра.

## Автор
Антяскин Максим

