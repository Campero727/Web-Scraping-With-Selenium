import argparse;
from selenium import webdriver;
from selenium.webdriver.support.ui import WebDriverWait;
from selenium.webdriver.support import expected_conditions as EC;
from selenium.webdriver.common.by import By;
from bs4 import BeautifulSoup;
import time;

def banner():
    print(" _____ _____ _____ _____ _____ ____  _____    __    _____ _____ _____ _____ ");
    print("|     |   __| __  |     |  _  |    \|     |  |  |  |     | __  | __  |   __|");
    print("| | | |   __|    -|   --|     |  |  |  |  |  |  |__|-   -| __ -|    -|   __|");
    print("|_|_|_|_____|__|__|_____|__|__|____/|_____|  |_____|_____|_____|__|__|_____|");
    print("                                                                            ");
def buscar(producto):
    try:
        options = webdriver.ChromeOptions();
        options.add_argument('--start-maximized');
        options.add_argument('--disable-extensions');
        driver_path = 'chromedriver.exe';
        driver = webdriver.Chrome(driver_path, chrome_options=options);
        driver.get('https://mercadolibre.com.mx');

        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input.nav-search-input'))).send_keys(producto);
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.nav-icon-search'))).click();
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div/div[1]/aside/div[3]/div[12]/ul/li[6]/form/button')));
        url = driver.find_element_by_xpath('/html/body/main/div/div[1]/aside/div[3]/div[12]/ul/li[6]/form/button').get_attribute("formaction");
        driver.get(url);

        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div/div[1]/section')));
        htlm_list = driver.find_element_by_css_selector("section.ui-search-results.ui-search-results--without-disclaimer");
        items_h2 = htlm_list.find_elements_by_css_selector("div.ui-search-result__wrapper");

        banner()
        print("\nResultados para la busqueda ",producto,'\n');

        for item in items_h2:
            tiulo = item.find_element_by_css_selector('h2.ui-search-item__title');
            txt_titulo = tiulo.get_attribute('innerHTML');
            precio = item.find_element_by_css_selector("span.price-tag-fraction");
            txt_precio = precio.get_attribute('innerHTML');
            url = item.find_element_by_css_selector("a.ui-search-link");
            txt_url = url.get_attribute('href');
            print("[+]Producto: ", txt_titulo);
            print("[+]Precio: ", txt_precio);
            print("[+]Url: ", txt_url);
            print('*' * 15, '\n' * 2);
        driver.close();
    except:
        print("Ha ocurrido un error inesperado Reejecuta el programa");

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Manual to this script')
    parser.add_argument('--product', type=str, default=None, help="Producto a buscar con el mayor descuento");
    args=parser.parse_args();
    if args.product:
        buscar(args.product);
    else:
        print("Ingresa un producto a buscar");