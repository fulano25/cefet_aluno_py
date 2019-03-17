import datetime
import pytz

# Refer to the Python quickstart on how to setup the environment:
# https://developers.google.com/calendar/quickstart/python
# Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
# stored credentials.
#
# event = {
#     'summary': 'Google I/O 2015',
#     'location': '800 Howard St., San Francisco, CA 94103',
#     'description': 'A chance to hear more about Google\'s developer products.',
#     'start': {
#         'dateTime': '2019-03-18T09:00:00-07:00',
#         'timeZone': 'America/Los_Angeles',
#     },
#     'end': {
#         'dateTime': '2019-03-18T17:00:00-07:00',
#         'timeZone': 'America/Los_Angeles',
#     },
#     'recurrence': [
#         'RRULE:FREQ=DAILY;COUNT=2'
#     ],
#     'attendees': [
#         {'email': 'lpage@example.com'},
#         {'email': 'sbrin@example.com'},
#     ],
#     'reminders': {
#         'useDefault': False,
#         'overrides': [
#         {'method': 'email', 'minutes': 24 * 60},
#         {'method': 'popup', 'minutes': 10},
#         ],
#     },
#     }
DUMMYDATA = {
    'id': '12345',
    'disciplina': 'ÁRVORES III',
    'turma': '666033',
    'status': 'Aceita/Matriculada',
    'hora_inicio': '12:40',
    'hora_fim':'15:20',
    'data_inicio_periodo': '05/12/18',
    'data_fim_periodo': '29/06/19',
    'dia_da_semana': '4', 
    'aula': 'Teórica',
    'nome_do_campus': 'Campus Maracanã',
    'nome_do_predio': 'Bloco Z',
    'numero_da_sala': 'E-666',
    'nome_do_docente': 'MARIA MIÇANGA DA PAZ'
    }
	
TIMEZONE = 'America/Sao_Paulo'

def create_event(data):
    start_datetime = gen_datetime(data['dia_da_semana'], data['hora_inicio'])
    end_datetime = gen_datetime(data['dia_da_semana'], data['hora_fim'])
    end_recurrence = expiration_date(data['data_fim_periodo'])
    summary = data['disciplina']
    campus = ''
    predio = ''
    sala = ''
    try: 
        campus = data['nome_do_campus']
    except:
        pass
    try:
        predio = data['nome_do_predio']
    except:
        pass
    try:
        sala = data['numero_da_sala']
    except:
        pass
    location = '{}: {} - {}'.format(campus, predio, sala)

    aula = ''
    docente = ''
    try:
        aula = data['aula'].lower()
    except:
        pass
    try:
        docente = data['nome_do_docente']
    except:
        pass
    description = 'Aula {} com prof. {}.'.format(aula, docente)

    return {
    'summary': summary,
    'location': location,
    'description': description,
    'start': {
        'dateTime': start_datetime,
        'timeZone': TIMEZONE,
    },
    'end': {
        'dateTime': end_datetime,
        'timeZone': TIMEZONE,
    },
    'recurrence': [
        'RRULE:FREQ=WEEKLY;UNTIL=' + end_recurrence 
    ],
    'reminders': {
        'useDefault': False,
        'overrides': [
        {'method': 'popup', 'minutes': 10},
        ],
    },
    }

def date_next_weekday(weekday):
    """
    weekday: int from 0 (monday) to 6 (sunday)
    Returns date of next weekday (2019-03-16)
    """
    today = datetime.date.today()
    today_weekday = today.weekday()
    days = int(weekday) - today_weekday
    if days < 0:
        days += 7
    return today + datetime.timedelta(days=days)

def datetime_now(tzone=TIMEZONE):
    tz = pytz.timezone(tzone)
    return datetime.datetime.now(tz)

def gen_datetime(weekday, time):
    """
    weekday: int from 0 (monday) to 6 (sunday)
    time: time string ('18:00')
    """
    date = date_next_weekday(weekday).strftime('%Y-%m-%d')
    return strfdatetime(date, time)

def strfdatetime(date, time):
    """
    Args
        date: str '2019-03-18'
        time: str '18:00'
    Returns:
        datetime: str '2019-03-18T17:00:00-03:00'
    """
    return date + 'T' + time + ':00' + datetime_now().strftime('%Z') + ':00'

def expiration_date(date):
    """
    Args
        date: str '17/03/19'
    Returns
        datetime: str '20110701T170000Z'
    """
    dt = datetime.datetime.strptime(date, '%d/%m/%y')
    return dt.strftime('%Y%m%dT%H%M%SZ')

if __name__ == '__main__':

    event = create_event(DUMMYDATA)

    print(event)