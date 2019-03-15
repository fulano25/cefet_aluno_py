from requests_html import HTMLSession
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from private import *
import os  


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

        self.print_table()
        # comp = list(PATH.keys())[2:11]
        # for f in comp:
        #     self.save_pdf(f)

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

    def get_page(self, path):
        url = urljoin(self.home.url, PATH[path] + self.matricula)
        return self.get(url)
    
    def save_pdf(self, file_name):
        response = self.get_page(file_name)
        content_type = response.headers.get('content-type')
        name = os.path.join(REL_DIR, file_name + '.pdf')
        if 'application/pdf' in content_type:
            with open(name, 'wb') as f:
                f.write(response.content)
        else:
            print('{}.pdf não disponível'.format(file_name))
    
    def print_table(self):
        r = self.get_page('quadro_horario')

        soup = BeautifulSoup(r.content, 'html5lib')
        tbody = soup.find('tbody')

        rows = []
        for row in tbody.find_all('tr'):
            r = []
            for val in row.find_all('td'):
                a = val.find('a')
                span = val.find('span', class_='label')
                if a:
                    a_dict = a.attrs
                    a_dict['content'] = ' '.join(a.text.split())
                    r.append(a_dict)
                elif span:
                    r.append(''.join(span.text.split()))
                else:
                    r.append('')
            rows.append(r)
            
        for r in rows:
            print(r)


if __name__ == '__main__':
    session = Session()