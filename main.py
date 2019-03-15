from requests_html import HTMLSession
from urllib.parse import urljoin
from private import *



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
    'notas': '/aluno/aluno/nota/nota.action?matricula=',
    'comunicados': '/comunicacoes/noticia/list.action?br.com.asten.si.geral.web.spring.interceptors.AplicacaoWebChangeInterceptor.aplicacaoWeb=1',

}

SITE = 'https://alunos.cefet-rj.br/'

class Session(HTMLSession):
    def __init__(self, url=SITE):
        super().__init__()
        self.get(url)
        self.password = PASSWORD
        self.username = USERNAME
        self.matricula = None
        self.home = self.login()
        try:
            matricula_element = self.home.html.find('#matricula', first=True)
            if matricula_element:
                self.matricula = matricula_element.attrs['value']
        except Exception as ex:
            print(ex)
        comp = ['atestado_trancamento', 'boletim_escolar', 'boletim_escolar_tecnico', 'comprovante_matricula', 'ficha_cadastral', 'integralizacao_curricular', 'solicitacao_matricula', 'comprovante_matricula_sie', 'historico_escolar_cr_aprovados']
        for f in comp:
            self.save_file(f)

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
    
    def save_file(self, file_name):
        response = self.get_page(file_name)
        with open(file_name + '.pdf', 'wb') as f:
            f.write(response.content)
    

if __name__ == '__main__':
    session = Session()