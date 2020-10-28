from .database import Database


class Client:

    def __init__(self):
        self.__db = Database('agronews')

    def checkIsActive(self, contact):
        """
        Verifica se o contato está cadastrado no nosso banco de dados.
        :param contact: Numero do contato
        :return: Retorna as info do contato.
        """
        res = self.__db.find_client(contact)
        if res:
            return {
                'nome': res[1],
                'recado': res[2],
                'numero': res[3],
                'step': res[4]
            }

    def newClient(self, nome, numero, recado):
        """
        Adiciona o contato ao nosso banco de dados.
        :param nome:
        :param numero: Numero do contato
        :param recado:
        :return:
        """
        return self.__db.insert_client(
            nome=nome,
            numero=numero,
            recado=recado
        )

    def changeStep(self, numero, step):
        return self.__db.update_step(
            numero=numero,
            step=step
        )

    def changeCulture(self, numero, cultura):
        return self.__db.update_cotacao(
            numero=numero,
            cotacao=cultura
        )

    def searchCulture(self, numero):
        res = self.__db.select_cotacao(
            numero=numero
        )
        return {
            'cultura': res[0]
        }
