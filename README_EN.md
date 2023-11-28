# University Schedule Integration
## Discription
This project is designed to automatically fetch and integrate a university schedule into Google Calendar. It uses Python with Selenium for web scraping and the Google Calendar API for calendar management. The script fetches a specific university schedule from a web page and inserts the events into a designated Google Calendar.

## Installation
To install the necessary dependencies, run the following command:
```
pip install -r requirements.txt
```
This will install packages like selenium, google-auth, and others required by the script.

## Setup
1. [Create a Google Cloud project](https://developers.google.com/workspace/guides/create-project)
  
2. Set up your environment:
     * In the Google Cloud console, [enable the Google Calendar API](https://console.cloud.google.com/flows/enableapi?apiid=calendar-json.googleapis.com)
     * [Configure the OAuth consent screen](https://developers.google.com/calendar/api/quickstart/python#configure_the_oauth_consent_screen)

3. Google Calendar API Setup:
    * Follow [Google's guide](https://developers.google.com/calendar/api/quickstart/python#authorize_credentials_for_a_desktop_application) to enable the Calendar API and obtain credentials.json 
    * Place credentials.json in the project's root directory.

4. Environment Variables:
    * Create a .env file in the project root directory.
    * Add your Google Calendar ID in the .env file as `calendarId=YOUR_CALENDAR_ID`.

5. [Download](https://chromedriver.chromium.org/downloads) the appropriate version of Selenium ChromeDriver and place it in the project root.

## Usage
To run the script, navigate to the project directory and execute:
```
python main.py
```
This will start the process of fetching the schedule and integrating it with your Google Calendar.
