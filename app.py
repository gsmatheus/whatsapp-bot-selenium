from src.whatsapp import WhatsApp
from src.client import Client


class App:

    def __init__(self):
        self.wpp = WhatsApp()
        self.client = Client()

    def run(self):
        """

        :return:
        """
        while True:

            # Percorre por todas as novas mensagens.
            for chat in self.wpp.latest_messages():

                # Verifica se o contato já está em nosso banco de dados.
                contato = self.client.checkIsActive(
                    contact=chat['numero']
                )

                if contato:

                    # Verifica qual o passo o contato está.
                    if contato['step'] == 0:  # Primeiro menu (escolher cotações ou noticias)
                        self.step0(contato)

                    elif contato['step'] == 1:  # Segundo menu
                        self.step1(contato, chat['mensagem'])

                    elif contato['step'] == 2:  # Terceiro menu
                        self.step2(contato, chat['mensagem'])

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

                        # Volta para a tela inicial do wpp.
                        self.wpp.home()

    def step0(self, contato):
        self.wpp.send_message(contato['numero'], f'Olá {contato["nome"]}, o que gostaria de saber hoje?%0a1 - Cotação')
        self.wpp.home()
        self.client.changeStep(contato['numero'], 1)

    def step1(self, contato, message):
        if message == '1':
            self.wpp.send_message(contato['numero'], '1 - Cotação de Soja?%0a2 - Cotação do Café%0a0 - Recomeçar')
            self.wpp.home()
            self.client.changeStep(contato['numero'], 2)

        else:
            self.invalidOption(contato['numero'])
            self.client.changeStep(contato['numero'], 1)

    def step2(self, contato, message):
        if message == '1':
            self.wpp.send_message(contato['numero'], 'Preço da soja é 9999.')
            self.wpp.home()

        elif message == '2':
            self.wpp.send_message(contact=contato['numero'], message='Preço do café é 9999.')
            self.wpp.home()

        elif message == '0':
            self.client.changeStep(contato['numero'], 1)
            self.step0(contato)

        else:
            self.invalidOption(contato['numero'])
            self.client.changeStep(contato['numero'], 2)

    def invalidOption(self, numero):
        self.wpp.send_message(
            contact=numero,
            message='Por favor escolha uma opção valida.'
        )
        self.wpp.home()


App().run()
