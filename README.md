# Интеграция Расписания Университета
## Описание
Этот проект предназначен для автоматического извлечения и интеграции расписания университета в Google Календарь. Он использует Python с Selenium для веб-скрапинга и API Google Календаря для управления календарем. 
Скрипт извлекает определенное расписание университета с веб-страницы и вставляет события в назначенный Google Календарь.

## Установка
Для установки необходимых зависимостей выполните следующую команду:
```
pip install -r requirements.txt
```

## Настройка
1. [Создайте проект Google Cloud](https://developers.google.com/workspace/guides/create-project)
  
2. Настройте вашу среду:
     * В консоли Google Cloud [включите API Google Календаря](https://console.cloud.google.com/flows/enableapi?apiid=calendar-json.googleapis.com)
     * [Настройте экран согласия OAuth](https://developers.google.com/calendar/api/quickstart/python#configure_the_oauth_consent_screen)

3. Настройка API Google Календаря:
    * Следуйте [руководству Google](https://developers.google.com/calendar/api/quickstart/python#authorize_credentials_for_a_desktop_application) для включения API Календаря и получения credentials.json
    * Разместите credentials.json в корневом каталоге проекта.
      
4. Переменные окружения:
   * Создайте файл .env в корневом каталоге проекта.
   * Добавьте ваш идентификатор Google Календаря в файл .env как `calendarId=YOUR_CALENDAR_ID`.

5. [Загрузите](https://chromedriver.chromium.org/downloads) подходящую версию ChromeDriver для Selenium и поместите ее в корневой каталог проекта.

## Использование
Чтобы запустить скрипт, перейдите в каталог проекта и выполните:
```
python main.py
```
