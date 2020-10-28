from src.whatsapp import WhatsApp
from src.client import Client
from src.cotacao import Cotacao

import json


class Menu:

    def __init__(self):
        with open('src/config/menu.json', encoding='utf-8') as json_file:
            self.config = json.load(json_file)

    def inicio(self, nome):
        menu = str(self.config['inicio']['descricao']).format(nome)
        for opcao in self.config['inicio']['opcoes']:
            menu += f"{opcao['id']} - {opcao['name']}%0a"

        return menu

    @property
    def cotacao(self):
        menu = ''
        for cultura in self.config['cotacao']:
            menu += f"{cultura['id']} - {cultura['name']}%0a"

        return menu


class App:

    def __init__(self):
        self.wpp = WhatsApp()
        self.client = Client()
        self.menu = Menu()

    def run(self):
        """

        :return:
        """
        while True:

            # Percorre por todas as novas mensagens.
            for chat in self.wpp.latest_messages():
                print(chat)

                # Verifica se o contato já está em nosso banco de dados.
                contato = self.client.checkIsActive(
                    contact=chat['numero']
                )

                if contato:

                    # Verifica qual o passo o contato está.
                    if contato['step'] == 0:  # Primeiro menu (escolher cotações ou noticias)
                        self.inicio(contato)

                    elif contato['step'] == 1:
                        self.passo1(contato, chat['mensagem'])

                    elif contato['step'] == 2:
                        self.passo2(contato, chat['mensagem'])

                    elif contato['step'] == 3:
                        self.passo3(contato, chat['mensagem'])

                # Verifica se a mensagem recebida é para ativar o bot.
                elif 'ativar' in chat['mensagem']:

                    # Coleta as informações do contato.
                    informacoes = self.wpp.contact_information(
                        contact=chat['numero']
                    )

                    # Verifica se obteve sucesso na coleta das informações.
                    if informacoes['status']:
                        # Adiciona o contato ao banco de dados.
                        self.client.newClient(
                            nome=informacoes['nome'],
                            recado=informacoes['recado'],
                            numero=chat['numero']
                        )

                        # Envia o primeiro menu
                        self.inicio({'numero': chat['numero'], 'nome': informacoes['nome']})

    def inicio(self, contato):
        self.wpp.send_message(contato['numero'], message=self.menu.inicio(nome=contato["nome"]))
        self.wpp.home()
        self.client.changeStep(contato['numero'], 1)

    def passo1(self, contato, mensagem):
        if mensagem == '1':
            self.wpp.send_message(contato['numero'], message=self.menu.cotacao)
            self.wpp.home()
            self.client.changeStep(contato['numero'], 2)

        else:
            self.invalidOption(contato['numero'])
            self.client.changeStep(contato['numero'], 1)

    def passo2(self, contato, mensagem):
        stop = False
        if not stop:
            if mensagem == '0':
                self.inicio(contato)
                stop = True

        for opcao in self.menu.config['cotacao']:
            if not stop:
                if mensagem == str(opcao['id']):
                    print(opcao)
                    self.wpp.send_message(contato['numero'], message=self.menu.config['mensagens']['passo3'])
                    self.wpp.home()
                    self.client.changeCulture(contato['numero'], cultura=opcao['keyword'])
                    self.client.changeStep(contato['numero'], 3)
                    stop = True

    def passo3(self, contato, mensagem):
        if mensagem == '1':
            self.wpp.send_message(contato['numero'],
                                  message=Cotacao(self.client.searchCulture(contato['numero'])['cultura'], qtd=1))
            self.wpp.home()

        elif mensagem == '2':
            self.wpp.send_message(contato['numero'],
                                  message=Cotacao(self.client.searchCulture(contato['numero'])['cultura']))
            self.wpp.home()

        elif mensagem == '0':
            self.passo1(contato, '1')

        else:
            self.invalidOption(contato['numero'])
            self.client.changeStep(contato['numero'], 3)

    def invalidOption(self, numero):
        self.wpp.send_message(
            contact=numero,
            message=self.menu.config['mensagens']['invalido']
        )
        self.wpp.home()


App().run()
