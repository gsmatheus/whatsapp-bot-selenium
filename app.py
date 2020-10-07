from src.whatsapp import WhatsApp

wpp = WhatsApp()

# Retorna uma lista com as mensagens novas. [contato , horario, mensagem]
print(wpp.latest_messages())
