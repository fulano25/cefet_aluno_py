from requests_html import HTMLSession
from urllib.parse import urljoin
from private import *

SITE = 'https://alunos.cefet-rj.br/'

class Session(HTMLSession):
    def __init__(self, url=SITE):
        super().__init__()
        self.get(url)
        self.password = PASSWORD
        self.username = USERNAME
        print(self.login().content)

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

if __name__ == '__main__':
    session = Session()