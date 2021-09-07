import os
from selenium.webdriver import Chrome
from selenium.webdriver import Edge
from selenium.webdriver import Opera
from xlsxwriter import Workbook
from win10toast import ToastNotifier

"""
import base
from selenium.common.exceptions import *
def exceute():
    driver = base.get_driver()
    filename = base.get_file_path(f'{__name__}')
    companies = []
    links = []

    driver.get('')
    companies_count = driver.find_elements_by_xpath('')
    for indx in range(1, len(companies_count) + 1):
        company_link = driver.find_element_by_xpath(f'').get_attribute('href')
        links.append(company_link)
    for link in links:
        company = {}

        try:
            driver.get(link)
            company_name = driver.find_element_by_xpath('').text
            company_email = driver.find_element_by_xpath('').text

            if '@' in company_email:
                company['Name'] = company_name
                company['Email'] = company_email
                companies.append(company)

        except NoSuchElementException:
            pass

    base.write_data(filename, companies)
    driver.close()
    return [True, __name__]
"""

trueMsg = "Successfuly"
falseMsg = "Failed"
browsers = {
    1: "Chrome",
    2: "Edge",
    3: "Opera"
}


def get_file_path(filename) -> str:
    outputfilename = f'data/{filename}.xlsx'
    return outputfilename


def notify(status: bool, filename: str, duration: int = 3):
    notifier = ToastNotifier()
    if status:
        msg = f'{filename} Scraping is successfully completed.'
    else:
        msg = f'{filename} Scraping is failed complete!'

    notifier.show_toast('Data scraping', msg, duration=duration)


def kill_web_driver_edge():
    try:
        os.system('taskkill /f /im MicrosoftWebDriver.exe')
    except Exception as ex:
        print(ex)


def get_driver(browser_id):
    browser_id = int(browser_id)
    if browser_id == 1:
        return Chrome(executable_path='drivers/chromedriver.exe')
    elif browser_id == 2:
        return Edge(executable_path='drivers/microsoftedgewebdriver.exe')
    elif browser_id == 3:
        return Opera(executable_path='drivers/operadriver.exe')


def write_data(filename, companies):
    row = 0
    workbook = Workbook(filename)
    worksheet = workbook.add_worksheet()
    worksheet.write(row, 0, "Adi")
    worksheet.write(row, 1, "Web site")
    worksheet.write(row, 2, "Ulke")
    worksheet.write(row, 3, "GSM")
    row += 1

    worksheet.set_column("A:B", 100)

    for company in companies:

        # First check if has null data.
        company_has_none_value = False
        for key in company:
            if company[key] is None:
                company_has_none_value = True
                continue

        if company_has_none_value:
            continue

        if "name" in company:
            worksheet.write(row, 0, company["name"])
        if "web_site" in company:
            worksheet.write(row, 1, company["web_site"])
        if "country_name" in company:
            worksheet.write(row, 2, company["country_name"])
        if "company_gsm" in company:
            worksheet.write(row, 3, company["company_gsm"])

        row += 1

    if not os.path.exists('data'):
        os.mkdir('data')

    if os.path.exists(filename):
        os.remove(filename)

    workbook.close()
