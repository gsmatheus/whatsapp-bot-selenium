from time import sleep


class WhatsApp:
    """
    Classe responsavel por executar as função do wpp no navegador
    """

    def __init__(self, browser):
        """
        :param browser: Recebe o objeto do selenium.
        """
        self.browser = browser

    def send_message(self, contact, message):
        """
        Função responsável por enviar uma nova mensagem.

        :param message: Mensagem que vai ser enviada para o contato.
        :param contact: Numero do contato.
        :return: Retorna uma dict com o status.
        """

        """
        Acessando o chat do contato com uma mensagem pré-definida.
        """
        try:
            self.browser.get(f'https://web.whatsapp.com/send?phone={contact}&text={message}')
            sleep(2)

            # Encontra o botão de enviar mensagem e clica sobre ele.
            button = self.browser.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button')
            button.click()
            sleep(1)

            return {
                'status': True
            }
        except Exception as e:
            return {
                'status': False,
                'message': str(e)
            }

    def get_info(self, contact):
        """
        Função que coleta algumas informações.

        :param contact: Numero do contato.
        :return: Retorna um dict com o status, nome e recado.
        """

        """
        Acessando a conversa do contato.
        """
        try:
            self.browser.get(f'https://web.whatsapp.com/send?phone={contact}')
            sleep(2)

            # Clicando sobre o numero.
            button = self.browser.find_element_by_xpath('//*[@id="main"]/header/div[2]')
            button.click()
            sleep(3.5)

            # Coletando o nome.
            name = self.browser.find_element_by_xpath(
                '//*[@id="app"]/div/div/div[2]/div[3]/span/div/span/div/div/div[1]/div[1]/div[2]/span/span').get_attribute(
                'textContent')

            # Coletando o recado.
            status = self.browser.find_element_by_xpath(
                '//*[@id="app"]/div/div/div[2]/div[3]/span/div/span/div/div/div[1]/div[4]/div[2]/div/div/span').get_attribute(
                'textContent')

            return {
                'status': True,
                'nome': name,
                'recado': str(status).replace('\u200e', '')
            }
        except Exception as e:
            return {
                'status': False,
                'message': str(e)
            }

    @property
    def home(self):
        """
        Função que retorna para a pagina inicial do WhatsApp.

        :return:
        """
        try:
            self.browser.get('https://web.whatsapp.com')
            self.browser.switch_to.alert.accept()
            sleep(1)
        except:
            pass
