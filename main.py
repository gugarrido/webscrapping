import time
import json
import xpath
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC


def waitUntil(driver, element_xpath, delay = 5):
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, element_xpath)))
        return True
    except TimeoutException:
        return False

def get_deputados_ids(driver):
    driver.get("https://www.camara.leg.br/deputados/quem-sao")
    deputados_ids = driver.find_element_by_xpath(xpath.OPTION_LABEL_IDS)
    deputados_ids_list = []

    [deputados_ids_list.append(x.get_attribute('value')) for x in deputados_ids.find_elements_by_xpath(".//*")]
    deputados_ids_list.pop(0)
    
    return deputados_ids_list


def access_deputados_page(deputados_ids_list, driver):
    deputados = {}
    for id in deputados_ids_list:
        driver.get(f"https://www.camara.leg.br/deputados/{id}")
        waitUntil(driver, xpath.DEPUTADO_PRESENCA)
        nome_deputado = driver.find_element_by_xpath(xpath.DEPUTADO_NOME).text
        deputado_presenca = driver.find_element_by_xpath(xpath.DEPUTADO_PRESENCA).text
        deputado_ausencia_just = driver.find_element_by_xpath(xpath.DEPUTADO_AUSENCIA_JUST).text
        deputado_ausencia_nao_just = driver.find_element_by_xpath(xpath.DEPUTADO_AUSENCIA_NAO_JUST).text
        deputado = {
            'nome': nome_deputado,
            'presenca': deputado_presenca,
            'ausencia_just': deputado_ausencia_just,
            'ausencia_nao_just': deputado_ausencia_nao_just,
        }
        deputados[id] = deputado

    with open('deputados_dict.json', 'w', encoding='utf-8') as file:
        json.dump(deputados, file, ensure_ascii=False, indent=4)

    driver.close()


def main():
    driver = webdriver.Firefox()
    access_deputados_page(get_deputados_ids(driver), driver)
if __name__ == "__main__":
    main()