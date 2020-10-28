from requests import get
from bs4 import BeautifulSoup


def CotacaoCepea1(tipo, qtd=0):
    count = 0
    retorno = []
    noticias = get(f'https://www.cepea.esalq.usp.br/br/indicador/{tipo}.aspx')
    page = BeautifulSoup(noticias.content, 'html.parser')
    cotacoes = page.find_all("table")[0]
    nota = page.find_all(attrs={"imagenet-fonte-tabela"})[1].text
    cotacaoIndividual = cotacoes.find_all("tr")
    for cotacao in cotacaoIndividual:
        if cotacao.find_all("td"):
            retorno.append(
                f"No dia *{cotacao.find_all('td')[0].text}* a cotação de {tipo} fechou em R$ {cotacao.find_all('td')[1].text} e US$ {cotacao.find_all('td')[4].text} com uma variação diária de {cotacao.find_all('td')[2].text} e mensal de {cotacao.find_all('td')[3].text}.\n%0a%0a_{nota}_\n%0a%0a")
            count = count + 1
            if count == qtd:
                break
    return retorno

    # Tipos que funcionam:
    # - acucar
    # - algodao
    # - arroz
    # - bezerro
    # - boi-gordo
    # - cafe
    # - soja


def Cotacao(tipo, qtd=0):
    if tipo == "todas":
        return '\r\n'.join(CotacaoCepea1('acucar', qtd)) + '\r\n'.join(CotacaoCepea1('algodao', qtd)) + '\r\n'.join(
            CotacaoCepea1('arroz', qtd)) + '\r\n'.join(CotacaoCepea1('bezerro', qtd)) + '\r\n'.join(
            CotacaoCepea1('boi-gordo', qtd)) + '\r\n'.join(CotacaoCepea1('cafe', qtd)) + '\r\n'.join(
            CotacaoCepea1('soja', qtd))
    else:
        return '\r\n'.join(CotacaoCepea1(tipo, qtd))
