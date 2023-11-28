import datetime as dt
import os
import os.path
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from selenium import webdriver
from selenium.webdriver.common.by import By

# Constants and Configurations
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

SCOPES = ["https://www.googleapis.com/auth/calendar"]
LINK = 'https://rasp.unecon.ru/raspisanie_grp.php?g=13181&w=15'
calendarId = os.getenv("calendarId")
REDUCTIONS = {
    'цифровые финансы': 'финансы',
    'анализ и экономическая оценка проектов': 'экономика',
    'промышленный интернет': 'пром инт',
    'инструментальные средства информационных систем': 'исис',
    'инфокоммуникационные системы и сети': 'инфокомм',
    'технологии облачных вычислений': 'облако',
    'Методы искусственного интеллекта ': 'ии',
    'физическая культура и спорт (элективные дисциплины)': 'физра',
}
CHOOSE = ['Анализ и экономическая оценка проектов', 'Цифровые финансы', 'Промышленный интернет']
UNTIL = '20231230'


def get_credentials():
    """Obtain the Google Calendar API credentials."""
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    else:
        creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds


def fetch_schedule(browser):
    """Fetch schedule from the web using Selenium."""
    schedule = []
    last_known_date = None

    browser.get(LINK)
    block = browser.find_element(By.TAG_NAME, "tbody")
    all_tr = block.find_elements(By.TAG_NAME, "tr")

    for tr in all_tr:
        class_attr = tr.get_attribute('class')
        all_td = tr.find_elements(By.TAG_NAME, "td")
        if tr.get_attribute('class') != 'new_day_border':
            date, time, lesson, last_known_date = extract_schedule_data(tr, all_td, last_known_date)
            if 'Выбор' in lesson and any(ch in lesson for ch in CHOOSE):
                lesson = lesson.replace('Выбор\n', '')
                schedule.append(lesson_to_schedule(date, time, lesson))
            elif class_attr == 'new_day' or class_attr == '':
                schedule.append(lesson_to_schedule(date, time, lesson))

    return schedule


def extract_schedule_data(tr, all_td, last_known_date):
    """Extract date, time, and lesson details from a table row."""

    if tr.get_attribute('class') == 'new_day':
        date = all_td[0].find_element(By.CLASS_NAME, 'date').get_attribute('innerText')
        last_known_date = date
    else:
        date = last_known_date

    time = all_td[1].find_element(By.CLASS_NAME, 'time').get_attribute('innerText')
    lesson = all_td[3].find_element(By.CLASS_NAME, 'predmet').get_attribute('innerText')

    return date, time, lesson, last_known_date


def lesson_to_schedule(date, time, lesson):
    """Convert lesson details to a schedule format."""
    if '(Лекция)' in lesson:
        lesson = lesson.replace('(Лекция)', '').lower()
    else:
        lesson = lesson.replace('(Практика)', '')

    replacement = REDUCTIONS.get(lesson.strip().lower())

    if replacement:
        lesson = replacement.capitalize() if lesson[0].isupper() else replacement

    day, month, year = date.split('.')
    start_time, end_time = time.split(' - ')

    return {
        'summary': lesson,
        'start': {
            'dateTime': f"{year}-{month}-{day}T{start_time}:00+03:00",
            'timeZone': 'Asia/Baghdad'
        },
        'end': {
            'dateTime': f"{year}-{month}-{day}T{end_time}:00+03:00",
            'timeZone': 'Asia/Baghdad'
        },
        'reminders': {
            'useDefault': True
        },
        'recurrence': [
            f'RRULE:FREQ=WEEKLY;INTERVAL=2;UNTIL={UNTIL}'
        ],
        'eventType': 'default'
    }


def list_of_events(service, dt, calendarId):
    """List upcoming events from the Google Calendar."""
    now = dt.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    print("Getting the upcoming 10 events")

    events_result = (
        service.events().list(
            calendarId=calendarId,
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        ).execute()
    )
    events = events_result.get("items", [])

    if not events:
        print("No upcoming events found.")
    else:
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            print(start, event["summary"])


def main():
    creds = get_credentials()

    try:
        service = build("calendar", "v3", credentials=creds)
        list_of_events(service, dt, calendarId)

        browser = webdriver.Chrome()
        schedule = fetch_schedule(browser)

        # insert events into the calendar
        for event in schedule:
            created_event = service.events().insert(calendarId=calendarId, body=event).execute()
            print(f"Event created: {created_event.get('htmlLink')}")

    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()
