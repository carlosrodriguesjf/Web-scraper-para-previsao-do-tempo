# PROJETO WEBSCRAPER PARA PREVISÃO DO TEMPO

# Importacoes
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions as EC
import smtplib
from email.message import EmailMessage
from time import sleep
from decouple import config


# Carregando constantes
EMAIL_ADDRESS = config('EMAIL_TESTES')
EMAIL_ADDRESS_SEND = config('MEU_EMAIL_PRINCIPAL')
EMAIL_PASSWORD = config('SENHA_EMAIL_TESTES')



def iniciar_driver():

    chrome_options = Options()

    arguments = ['--lang=pt-BR', '--start-maximized','--incognito']

    for argument in arguments:
        chrome_options.add_argument(argument)

    driver = webdriver.Chrome(options=chrome_options)

    wait = WebDriverWait(
        driver, 
        10, 
        poll_frequency = 1,
        ignored_exceptions = [
            NoSuchElementException,
            ElementNotVisibleException,
            ElementNotSelectableException,
            InvalidSessionIdException,
            TimeoutException
        ]
    )

    return driver, wait


def coleta_de_dados(driver, wait):
    dados_previsao_tempo = []

    driver.execute_script("window.scrollTo(0, 1500);")

    sleep(2)

    # Coletando as informações:
    print('Coletando as informações...')
    for i in range(1,5):

        # Coletando as informações de hoje:

        # Data de extração
        data_extracao = driver.find_element(By.XPATH,f"//div[@class='daily-list-body']/a[{i}]/div[1]/p[2]").text
        #data_extracao = wait.until(EC._element_if_visible((By.XPATH,f"//div[@class='daily-list-body']/a[{i}]/div[1]/p[2]")))

        # Extraindo a temperatura atual.
        temperatura = driver.find_element(By.XPATH,f"//div[@class='daily-list-body']/a[{i}]/div[2]//div/span").text

        # # Extraindo a condição do tempo atual (ex. ensolarado, nublado, etc.).
        condicao_tempo = driver.find_element(By.XPATH,f"//div[@class='daily-list-body']/a[{i}]/div[3]/p").text

        dados_previsao_tempo.append([data_extracao, temperatura, condicao_tempo])
        #dados_previsao_tempo.append([data_extracao])


    return dados_previsao_tempo


def envio_email(EMAIL_ADDRESS, EMAIL_ADDRESS_SEND, EMAIL_PASSWORD,relatorio):

    print('Enviando o email...')

    # Criar e enviar um email
    mail = EmailMessage()
    mail['Subject'] = 'Dados previsão do tempo'


    mail['From'] = EMAIL_ADDRESS
    mail['To'] = EMAIL_ADDRESS_SEND
    mail.set_content(relatorio)

    # Enviar o email
    with smtplib.SMTP_SSL('smtp.gmail.com',465) as email:
        email.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
        email.send_message(mail)


def formata_email(dados_previsao_tempo):
    relatorio = 'Seguem os dados da previsão do tempo de hoje e dos próximos 3 dias:\n\n'
    for dia in dados_previsao_tempo:
        relatorio += f"Data: {dia[0]}\n"
        relatorio += f"Temperatura: {dia[1]}\n"
        relatorio += f"Condições: {dia[2]}\n\n"
    return relatorio



##1. NAVEGAÇÃO AUTOMÁTICA
# Abrindo um navegador e acessar um site de previsão do tempo
#Iremos utilizar o site https://www.accuweather.com/

print('Abrindo o site...')
driver, wait = iniciar_driver()
driver.get('https://www.accuweather.com/pt/br/juiz-de-fora/33806/weather-forecast/33806')


###2. COLETA DOS DADOS METEREOLÓGICOS

dados_previsao_tempo =  coleta_de_dados(driver, wait)



###3. TRATAMENTO E FORMATAÇÃO DE DADOS
#- Organizar os dados extraídos em um formato legível.

relatorio = formata_email(dados_previsao_tempo)



###4. ENVIO DE E-MAIL

envio_email(EMAIL_ADDRESS, EMAIL_ADDRESS_SEND, EMAIL_PASSWORD, relatorio)

print('Programa finalizado!')
