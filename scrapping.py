from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
import smtplib

def scrapping_cesal():
    
    email = "***"
    password = "***"
    date_fin_bail = "14/04/2023"
    Res = []

    options = Options()
    options.add_argument("start-maximized")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("enable-automation")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_experimental_option('excludeSwitches', ['disable-popup-blocking','enable-automation', 'enable-logging'])
    

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try : 
        url = "https://logement.cesal.fr/espace-resident/cesal_login.php" 
        driver.get(url)
        time.sleep(1)
                
        button_con = driver.find_element("id", "button_connexion")
        button_con.click()
        time.sleep(1)
        
        #Connexion
        search_email = driver.find_element(By.ID, "login-email")
        search_email.send_keys(email)

        search_password = driver.find_element(By.ID, "login-password")
        search_password.send_keys(password)

        time.sleep(1)
        
        # search_password.send_keys(Keys.RETURN)
        button_valida = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="connexion"]/form/div[4]/div/button')))
        button_valida.click()
        time.sleep(1)
        
        button_res = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, 'Réserver')))
        button_res.click()
        
        time.sleep(1)

        #choix date arrivée/fin du bail
        search_date_debut = driver.find_element("id", "select2-date_arrivee-container")
        search_date_debut.click()
        inp = driver.find_element(By.XPATH, "/html/body/span/span/span[1]/input")
        inp.send_keys("2022")
        inp.send_keys(Keys.RETURN)

        
        search_date_fin = driver.find_element("id", "date_sortie")
        search_date_fin.send_keys(date_fin_bail)
        search_date_fin.send_keys(Keys.RETURN)
        search_date_fin.send_keys(Keys.RETURN)
        
        time.sleep(1)
        #res1 = driver.find_element("id", "residence_1_logements_disponibles")
        #Res.append(res1.text)
        #res2 = driver.find_element("id", "residence_2_logements_disponibles")
        #Res.append(res2.text)
        #res3 = driver.find_element("id", "residence_3_logements_disponibles")
        #Res.append(res3.text)
        res4 = driver.find_element("id", "residence_4_logements_disponibles")
        Res.append(res4.text)
        #res5 = driver.find_element("id", "residence_5_logements_disponibles")
        #Res.append(res5.text)
        #res6 = driver.find_element("id", "residence_6_logements_disponibles")
        #Res.append(res6.text)
    
        driver.quit()
        
        return Res
    
    except : 
        driver.quit()
        return "Error"


def Flag_logement_dispo(Liste):
    if Liste == ["Aucune logement disponible"] :
        return False
    return True


def envoi_mail(objet, texte):
    
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    SMTP_USERNAME = "***"
    SMTP_PASSWORD = "***"
    EMAIL_FROM = "***"
    EMAIL_TO = "***"
    EMAIL_SUBJECT = objet
    EMAIL_MESSAGE = texte
    
    s = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    s.starttls()
    s.login(SMTP_USERNAME, SMTP_PASSWORD)
    message = 'Subject: {}\n\n{}'.format(EMAIL_SUBJECT, EMAIL_MESSAGE)
    s.sendmail(EMAIL_FROM, EMAIL_TO, message)
    s.quit()
    
    return


def main():
    liste = scrapping_cesal()
    
    if liste == "Error" :
        envoi_mail("PROBLEME CODE SCRAPPING CESAL", "Probleme de connexion au site de cesal")
        print("erreur code")
        return
    
    if Flag_logement_dispo(liste) : 
        envoi_mail("ALERTE LOGEMENT DISPO", "Il y a des logements dispo sur Cesal - Espace resident")
        print("logement dispo")
        return
    print("Nothing new")
    return
main()