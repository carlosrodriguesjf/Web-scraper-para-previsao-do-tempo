# PROJETO WEBSCRAPER PARA PREVISÃO DO TEMPO

#importacoes
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep




def iniciar_driver():

    chrome_options = Options()

    arguments = ['--lang=pt-BR', '--start-maximized','--incognito']

    for argument in arguments:
        chrome_options.add_argument(argument)

    driver = webdriver.Chrome(options=chrome_options)
    return driver


def coleta_de_dados():
    dados_previsao_tempo = []

    sleep(5)

    # Coletando as informações:
    print('Coletando as informações...')
    for i in range(1,5):

        # Coletando as informações de hoje:

        # Data de extração
        data_extracao = driver.find_element(By.XPATH,f"//a[@class='daily-list-item '][{i}]/div/p[2]").text

        # Extraindo a temperatura atual.
        temperatura = driver.find_element(By.XPATH,f"//a[@class='daily-list-item '][{i}]/div/div/span").text

        # Extraindo a condição do tempo atual (ex. ensolarado, nublado, etc.).
        condicao_tempo = driver.find_element(By.XPATH,f"//a[@class='daily-list-item '][{i}]/div[@class='phrase']/span/p").text

        dados_previsao_tempo.append([data_extracao, temperatura, condicao_tempo])

        sleep(2)

    return dados_previsao_tempo


###1. NAVEGAÇÃO AUTOMÁTICA
# Abrindo um navegador e acessar um site de previsão do tempo
#Iremos utilizar o site https://www.accuweather.com/


#acessando o site
print('Abrindo o site...')

driver = iniciar_driver()
driver.get('https://www.accuweather.com/pt/br/juiz-de-fora/33806/weather-forecast/33806')



###2. COLETA DOS DADOS METEREOLÓGICOS

dados_previsao_tempo =  coleta_de_dados()

print(dados_previsao_tempo)


driver.close()