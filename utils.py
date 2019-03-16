from unicodedata import normalize


def remover_acentos(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('utf-8') 

def trim(s, separator=' '):
    return separator.join(s.split())

def trim_text(s, separator=' '):
    return separator.join(s.text.split())

def format_key(val):
    if val:
        if ' ' in val:
            val = trim(val, separator='_')
        return remover_acentos(val).lower()
    else:
        return ''

def list_from_table(table, th_func=trim_text, td_func=trim_text):
    thead = table.find('thead')
    header = []
    body = []
    if thead:
        tr = thead.find('tr')
        header = [th_func(i) for i in tr.find_all('th')]
    tbody = table.find('tbody')
    if tbody:
        for row in tbody.find_all('tr'):
            r = [td_func(i) for i in row.find_all('td')]
            body.append(r)
    return [header, *body]

def tuples_to_dict(lst):
    keys = [format_key(i) for i in list(dict(lst).keys())]
    values = [i.strip() for i in list(dict(lst).values())]
    return dict(zip(keys, values))

def table_to_dicts(lst):
    keys = [format_key(i) for i in lst[0]]
    dict_list = []
    for row in lst[1::]:
        values = row
        dict_list.append(dict(zip(keys, values)))
    return dict_list

def handle_timetable_th(th):
    label = th.find('span', class_='label')
    if label:
        return format_key(label.text)
    else:
        return 'horario'
        
def handle_timetable_td(td):
    a = td.find('a')
    img = td.find('img')
    span = td.find('span', class_='label')
    if a:
        a_dict = a.attrs
        identifier = a_dict['href'].split('=')[1]
        _nome, _turma = trim_text(a).split(' T. ')
        nome = {'nome': _nome}
        turma = {'turma': _turma}
        status = {'status': img.attrs['title']}
        data, hora = a_dict['title'].split(' > ')
        hora = hora.split('Horário: ')[1]
        _hora_inicio, _hora_fim = hora.split(' às ')
        data = data.split('Período: ')[1]
        _data_inicio_periodo, _data_fim_periodo = data.split(' - ')
        hora_inicio = {'hora_inicio': _hora_inicio}
        hora_fim = {'hora_fim': _hora_fim}
        data_inicio_periodo = {'data_inicio_periodo': _data_inicio_periodo}
        data_fim_periodo = {'data_fim_periodo': _data_fim_periodo}
        ident = {'id': identifier}
        d = {**ident, **nome, **turma, **status, **a_dict, **hora_inicio,
            **hora_fim, **data_inicio_periodo, **data_fim_periodo}
        # cleaning up
        d.pop('href', None)
        d.pop('target', None)
        d.pop('title', None)
        return d
    elif span:
        return trim_text(span, separator='')
    else:
        return ''

if __name__ == '__main__':
    pass