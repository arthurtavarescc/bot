from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys
import random

def dividir_texto_em_partes(texto, num_partes=6):
    # Adiciona uma quebra de linha antes de cada danda "।"
    texto_com_quebra = texto.replace("।", "\n।")

    # Divide o texto em frases após adicionar a quebra de linha
    frases = [frase.strip() for frase in texto_com_quebra.split("\n") if frase.strip()]
    total_frases = len(frases)

    # Determina o tamanho de cada parte
    tamanho_parte = total_frases // num_partes
    sobra = total_frases % num_partes

    partes = []
    inicio = 0

    # Divide em partes equilibradas
    for i in range(num_partes):
        fim = inicio + tamanho_parte + (1 if i < sobra else 0)
        parte = "\n".join(frases[inicio:fim]) if inicio < fim else ""
        partes.append(parte)
        inicio = fim

    return partes

def traduzir_parte(driver, parte, indice):
    """
    Função para traduzir uma parte do texto.
    """
    try:
        # Localiza e insere o texto no campo de entrada
        campo_texto = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[data-testid='translation-input']"))
        )
        campo_texto.send_keys(Keys.CONTROL + "a")  # Seleciona todo o texto
        campo_texto.send_keys(Keys.DELETE)
        time.sleep(1)
        campo_texto.send_keys(parte)

        # Localiza e clica no botão de tradução
        botao_traduzir = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Translate']"))
        )
        botao_traduzir.click()
        while True:
            a = tratamento_wrong(driver)
            if a: break
            else:
                return traduzir_parte(driver, parte, indice)

        monitorar_div_pai(driver)

        # Aguarda o resultado da tradução
        traducoes = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "p.MuiTypography-body1"))
        )
        texto_traduzido = "\n".join(
            [p.text for p in traducoes if p.text.strip() not in ["Transliteration", "Output language"]]
        )

        return f"{texto_traduzido}"

    except Exception as e:
        print(f"Erro ao traduzir a parte {indice}: {e}")
        return f"Parte {indice}:\n[Erro na tradução]\n\n"


def tratamento_wrong(driver):
    """Verifica se os servidores estão sobrecarregados."""
    try:
        # Localiza a mensagem de erro
        elemento = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//p[contains(@class, "MuiTypography-root") and contains(@class, "MuiTypography-alignCenter")]'))
        )
        if "Our servers are currently under a high load." in elemento.text:
            print("Servidor sobrecarregado. Recarregando a página...")
            driver.refresh()
            time.sleep(random.randint(3, 5))  # Tempo aleatório para evitar bloqueios
            return False
    except:
        # Se não encontrar a mensagem de erro, continua o programa
        return True



def monitorar_div_pai(driver, tempo_espera=2, intervalo=0.2):
    """
    Monitora uma div pai e verifica se ela parou de ser criada/modificada.

    :param driver: Instância do Selenium WebDriver.
    :param seletor_pai: Seletor CSS da div pai.
    :param tempo_espera: Tempo de espera após detectar que a div não mudou mais.
    :param intervalo: Intervalo entre verificações.
    """
    try:
        # Aguarda a div pai aparecer inicialmente
        div_pai = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.MuiBox-root.mui-0"))
        )

        # Variáveis de controle
        html_anterior = ""
        tempo_final = 0

        while True:
            # Captura o HTML atual da div
            html_atual = div_pai.get_attribute("innerHTML")

            # Verifica se o conteúdo da div parou de mudar
            if html_atual == html_anterior:
                if tempo_final == 0:  # Marca o início do tempo de espera
                    tempo_final = time.time()
                elif time.time() - tempo_final >= tempo_espera:
                    break
            else:
                # Resetando se houve modificação
                html_anterior = html_atual
                tempo_final = 0  # Reseta o tempo de espera

            time.sleep(intervalo)  # Intervalo entre verificações

    except Exception as e:
        print(f"Erro: {e}")
