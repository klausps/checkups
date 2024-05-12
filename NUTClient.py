import socket

class NUTClient:
    def __init__(self, host, port=3493, debug=False):
        self.host = host
        self.port = port
        self.socket = None
        self.debug = debug  # Adiciona uma variável de debug

    def connect(self):
        """Estabelece conexão com o servidor NUT."""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.socket.settimeout(5)
            if self.debug:
                print('Conectado ao servidor, enviando comando HELP...')
            self._send_command('HELP')  # Solicita comandos disponíveis como handshake
            if self.debug:
                print('Resposta inicial do servidor:', self._receive_response())
            else:
                self._receive_response()  # Receber resposta sem imprimir
            if self.debug:
                print('Conexão estabelecida com sucesso.')
        except Exception as e:
            if self.debug:
                print('Falha ao conectar ao servidor NUT:', e)
            self.close()
            exit(1)

    def login(self, username, password):
        """Realiza autenticação no servidor NUT."""
        self._send_command(f'USERNAME {username}')
        response = self._receive_response()
        if 'OK' in response:
            self._send_command(f'PASSWORD {password}')
            response = self._receive_response()
            if 'OK' in response:
                if self.debug:
                    print('Autenticação bem-sucedida.')
            else:
                if self.debug:
                    print('Falha na autenticação: senha incorreta.')
                self.close()
                exit(1)
        else:
            if self.debug:
                print('Falha na autenticação: usuário incorreto.')
            self.close()
            exit(1)

    def get_var(self, upsname, varname):
        """Obtém o valor de uma variável de um UPS específico."""
        self._send_command(f'GET VAR {upsname} {varname}')
        response = self._receive_response()
        if response.startswith('VAR'):
            return response.split(' ')[3].strip('\"')  # Remove aspas se presentes
        elif 'ERR UNKNOWN-UPS' in response:
            if self.debug:
                print(f'Erro: O UPS "{upsname}" não é conhecido. Verifique o nome e tente novamente.')
            return None
        else:
            raise Exception('Erro ao obter variável: ' + response)

    def _send_command(self, command):
        """Envia um comando ao servidor NUT."""
        self.socket.sendall((command + '\n').encode('utf-8'))

    def _receive_response(self):
        """Recebe a resposta do servidor."""
        response = ""
        try:
            while True:
                part = self.socket.recv(1024).decode('utf-8')
                response += part
                if len(part) < 1024:
                    break
            return response.strip()
        except socket.error as e:
            if self.debug:
                print('Erro ao receber dados:', e)
            raise e

    def close(self):
        """Fecha a conexão com o servidor."""
        if self.socket:
            self.socket.close()
            if self.debug:
                print('Conexão fechada.')