from requests_html import HTMLSession
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from private import *
from utils import *
import os
from datetime import datetime

PATH = {
    'matricula': '/aluno/aluno/matricula/solicitacoes.action?matricula=',
    
    'relatorios': '/aluno/aluno/relatorio/relatorios.action?matricula=',
    'atestado_trancamento': '/aluno/aluno/relatorio/atestadoTrancamento.action?matricula=',
    'boletim_escolar': '/aluno/aluno/relatorio/boletimEscolar.action?matricula=',
    'boletim_escolar_tecnico': '/aluno/aluno/relatorio/boletimEscolarTecnico.action?matricula=',
    'comprovante_matricula': '/aluno/aluno/relatorio/comprovanteMatricula.action?matricula=',
    'ficha_cadastral': '/aluno/aluno/relatorio/fichaCadastral.action?matricula=',
    'integralizacao_curricular': '/aluno/aluno/relatorio/integralizacaoCurricular.action?matricula=',
    'solicitacao_matricula': '/aluno/aluno/relatorio/solicitacaoMatricula.action?matricula=',
    'comprovante_matricula_sie': '/aluno/aluno/relatorio/com/comprovanteMatricula.action?matricula=',
    'historico_escolar_cr_aprovados': '/aluno/aluno/relatorio/com/historicoEscolarCRAprovados.action?matricula=',

    'horarios': '/aluno/aluno/quadrohorario/menu.action?matricula=',
    'quadro_horario': '/aluno/ajax/aluno/quadrohorario/quadrohorario.action?matricula=',
    'notas': '/aluno/aluno/nota/nota.action?matricula=',
    'comunicados': '/comunicacoes/noticia/list.action?br.com.asten.si.geral.web.spring.interceptors.AplicacaoWebChangeInterceptor.aplicacaoWeb=1',

}

SITE = 'https://alunos.cefet-rj.br/'

REL_DIR = './rel'

class Session(HTMLSession):
    def __init__(self, url=SITE):
        super().__init__()
        self.get(url)
        self.password = PASSWORD
        self.username = USERNAME
        self.matricula = None
        self.home = self.login()
        
        if not os.path.isdir(REL_DIR):
            os.makedirs(REL_DIR)

        matricula_element = self.home.html.find('#matricula', first=True)
        if matricula_element:
            self.matricula = matricula_element.attrs['value']
        else:
            raise Exception('matrícula não encontrada')

    def login(self):
        """
        Sends a POST request. Returns Response object.
        """
        url = urljoin(SITE, 'aluno/j_security_check')
        data = {
            'j_username': self.username,
            'j_password': self.password
            }
        return self.post(url, data=data)

    def get_url(self, path):
        url = urljoin(self.home.url, path)
        return self.get(url)

    def get_page(self, item):
        return self.get_url(PATH[item] + self.matricula)
    
    def get_timetable_list(self):
        r = self.get_page('quadro_horario')
        soup = BeautifulSoup(r.content, 'html5lib')
        table = soup.find('table')
        l = list_from_table(table, th_func=handle_timetable_th,
            td_func=handle_timetable_td)
        
        table_list = [l[0]]
        for r in l[1::]:
            new_row = []
            for c, col in enumerate(r):
                if col and not isinstance(col, str):
                    # monday is 0 / segunda-feira é 0
                    new_col = {**col, **{'dia_da_semana': str(c-2)}}
                    new_row.append(new_col)
                else:
                    new_row.append(col)
            table_list.append(new_row)

        return table_list

    def get_timetable_dict(self): 
        table = self.get_timetable_list()
        return table_to_dicts(table)
    
    def get_timetable_entries(self):
        timetable = self.get_timetable_list()
        entries = []
        for row in timetable[1::]:
            for item in row[1::]:
                if item:
                    entries.append(item)

        return entries

    def get_class(self, identifier):
        url = '/aluno/aluno/turma.action?turma=' + str(identifier)
        ident = {'id': str(identifier)}
        r = self.get_url(url)
        soup = BeautifulSoup(r.content, 'html5lib')
        tables = soup.find_all('table')
        tur = soup.find('div', class_='topopage')
        num_turma = trim(tur.text).split()[-1]
        turma = {'turma': num_turma}

        discip = tables[1]
        discip.tr.extract()
        disciplina = sum(list_from_table(discip), [])
        disc_tupl = []
        for i in disciplina:
            if ':' in i:
                o = i.split(':')
            else:
                o = i.split(' ', 1)
            disc_tupl.append(o)

        t5 = list_from_table(tables[5])
        if len(t5[1]) > 4:
            esp_fisico = [t5[0], t5[1][0:5], [t5[1][0], *t5[1][4::]]] 
        else:
            esp_fisico = t5

        geral = {**ident, **turma, **tuples_to_dict(disc_tupl)}
        vagas = tuples_to_dict(list_from_table  (tables[2])[2::])
        docente = table_to_dicts(list_from_table(tables[3]))
        horarios = table_to_dicts(list_from_table(tables[4]))
        espaco_fisico = table_to_dicts(esp_fisico)

        return {'geral': geral, 'vagas': vagas, 'docente': docente,
                'horarios': horarios, 'espaco_fisico': espaco_fisico}

    def save_pdf(self, file_name):
        response = self.get_page(file_name)
        content_type = response.headers.get('content-type')
        name = os.path.join(REL_DIR, file_name + '.pdf')
        if 'application/pdf' in content_type:
            with open(name, 'wb') as f:
                f.write(response.content)
            log_message = '{}.pdf salvo com sucesso'.format(file_name)
        else:
            log_message = '{}.pdf não disponível'.format(file_name)
        return log_message 

    def save_all_docs(self):
        log_path = os.path.join(REL_DIR, 'log.txt')
        if os.path.isfile(log_path):
            os.remove(log_path)
        pdfs = list(PATH.keys())[2:11]
        for pdf in pdfs:
            log_message = self.save_pdf(pdf)
            time = datetime.now().strftime('%H:%M:%S-%d/%m/%Y')
            with open(log_path, 'a') as f:
                f.write(time + ' ' + log_message + '\n')


if __name__ == '__main__':
    session = Session()

    session.save_all_docs()

    data = {'timetable_entries': session.get_timetable_entries(),
            'timetable_list': session.get_timetable_list(),
            'a_class_example': session.get_class(76101)}
    
    import json

    JSON_DIR = './json'

    if not os.path.isdir(JSON_DIR):
        os.makedirs(JSON_DIR)

    for f, d in data.items():
        name = os.path.join(JSON_DIR, f + '.json')
        with open(name, 'w') as outfile:  
            json.dump(d, outfile)
    
    print('Done!')