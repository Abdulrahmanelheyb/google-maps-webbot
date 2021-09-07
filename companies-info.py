import time
import base
from selenium.common.exceptions import *


def exceute():
    driver = base.get_driver()
    filename = base.get_file_path(f'companies-info')
    companies = []
    links = []

    driver.get('https://www.google.com/maps/search/Bursa+wordpress/@40.204474,29.0049035,12z')
    time.sleep(3)

    while True:
        # Scroll down companies list
        companies_count = len(driver.find_elements_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[4]/div[1]/div'))
        prev_count = 0
        while companies_count > prev_count:
            prev_count = companies_count
            parent = driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[4]/div[1]')
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", parent)
            time.sleep(1)
            companies_count = len(driver.find_elements_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[4]/div[1]/div'))

        # Get companies
        for indx in range(1, companies_count + 1):
            try:
                company_link = driver.find_element_by_xpath(f'//*[@id="pane"]/div/div[1]/div/div/div[4]/div[1]/div[{indx}]/div/a').get_attribute('href')
                links.append(company_link)
            except Exception:
                pass

        if driver.find_element_by_xpath('//*[@id="ppdPk-Ej1Yeb-LgbsSe-tJiF1e"]').is_enabled():
            driver.find_element_by_xpath('//*[@id="ppdPk-Ej1Yeb-LgbsSe-tJiF1e"]').click()
        else:
            break

    for link in links:
        company = {}

        try:
            driver.get(link)
            time.sleep(2)

            name = None
            web_site = None
            country_name = None
            gsm = None

            try:
                name = driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[1]/h1/span[1]')
                if name.text:
                    name = name.text
                else:
                    name = ''
            except NoSuchElementException:
                pass

            info_section_count = len(driver.find_elements_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[7]/div'))
            for indx in range(1, info_section_count + 1):

                try:
                    path = f'//*[@id="pane"]/div/div[1]/div/div/div[7]/div[{indx}]/button'
                    res = driver.find_element_by_xpath(path).get_attribute('aria-label')
                    if 'Adres:' in res:
                        res = res.replace('Adres:', '')
                        if '/' in res:
                            res = res.split('/')
                            res = res[1].split(',')
                            country_name = res[1]
                            continue
                        elif ',' in res:
                            res = res[1].split(',')
                            country_name = res[1]
                            continue

                    if 'Web sitesi:' in res:
                        res = res.replace('Web sitesi:', '')
                        web_site = res
                        continue

                    if 'Telefon:' in res:
                        res = res.replace('Telefon:', '')
                        gsm = res
                        continue

                except Exception as ex:
                    print(ex)
                    pass

            # company_email = driver.find_element_by_xpath('')

            company['name'] = name
            # company['email'] = company_email
            company['web_site'] = web_site
            company['country_name'] = country_name
            company['company_gsm'] = gsm
            companies.append(company)

        except NoSuchElementException:
            pass

    base.write_data(filename, companies)
    driver.close()
    return [True, __name__]


exceute()
