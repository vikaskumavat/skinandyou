from google.oauth2.credentials import Credentials

user_credentials = Credentials.from_authorized_user_file('google_creds/token.json')
from googleapiclient.discovery import build


service = build('calendar', 'v3', credentials=user_credentials)
'''
event = {
  'summary': 'Hi, You have an Appointment With Patient : Shilpa Shinde and Mobile: 7418529630',
  'location': 'Test Line 1',
  'description': 'Test Line 2 Description',
  'start': {
    'dateTime': '2023-12-22T12:00:00+05:30',
    'timeZone': 'Asia/Kolkata',
  },
  'end': {
    'dateTime': '2023-12-22T13:00:00+05:30',
    'timeZone': 'Asia/Kolkata',
  },
#   'recurrence': [
#     'RRULE:FREQ=DAILY;COUNT=2'
#   ],
  'attendees': [
    {'email': 'arjungupta668@gmail.com'},
    # {'email': 'marketing@skinandyou.in'},
  ],
  'reminders': {
    'useDefault': False,
    'overrides': [
    #   {'method': 'email', 'minutes': 24 * 60},
      {'method': 'popup', 'minutes': 30},
    ],
  },
}
'''


event = {
    'summary': 'Hi, You have an Appointment With Patient : Shilpa Shinde and Mobile: 7418529630',
    'location': 'Nariman Point Clinic',
    'description': 'Disease: Testing Google Calendar',
    'start': {
        'dateTime': '2023-12-24T15:26:00+05:30',
        'timeZone': 'Asia/Kolkata'
    },
    'end': {
        'dateTime': '2023-12-24T16:26:00+05:30',
        'timeZone': 'Asia/Kolkata'
    },
    'attendees': [
        {
        'email': 'arjungupta668@gmail.com'
        }
    ],
    'reminders': {
            'useDefault': False,
            'overrides': [
                {
                    'method': 'popup',
                    'minutes': 30
                }
            ]
        }
    }

event = service.events().insert(calendarId='primary', body=event).execute()

print("Event === \n\n\n ", event.get('htmlLink'))
