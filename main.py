from cefet_aluno import Session
from models import create_event
from google_api import create_gcal_service


if __name__ == '__main__':
    session = Session()
    classes = session.get_detailed_classes()

    events = []
    for i in classes:
        events.append(create_event(i))

    service = create_gcal_service()
    
    for ev in events:
        event = service.events().insert(calendarId='primary', body=ev).execute()
        print('Event created: {}'.format(event.get('htmlLink')))



    

