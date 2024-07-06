import time
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions

options = Options()
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://ieeexplore.ieee.org/Xplore/home.jsp")

search_xpath = '//*[@id="LayoutWrapper"]/div/div/div[3]/div/xpl-root/header/xpl-header/div/div[2]/div[2]/xpl-search-bar-migr/div/form/div[2]/div/div[1]/xpl-typeahead-migr/div/input'
element = driver.find_element(By.XPATH, search_xpath)
element.send_keys("Artificial Intelligence")
element.send_keys(Keys.ENTER)

def get_article_info():
    article_info = {}

    buttons = driver.find_elements(By.XPATH, '//*[@id="xplMainContentLandmark"]/div/xpl-document-details/div/div[1]/section[2]/div/xpl-document-header/section/div[2]/div/div/div[3]/div[2]/div[1]/div[1]/button')
    number_of_buttons = len(buttons)
    cites_in_papers = None
    cites_in_patents = None
    full_text_views = None

    for page_btn in range(1, number_of_buttons + 1):
        btn_xpath = f'//*[@id="xplMainContentLandmark"]/div/xpl-document-details/div/div[1]/section[2]/div/xpl-document-header/section/div[2]/div/div/div[3]/div[2]/div[1]/div[1]/button[{page_btn}]/div[1]'
        btn_value = driver.find_element(By.XPATH, btn_xpath).text
        button = driver.find_element(By.XPATH, f'//*[@id="xplMainContentLandmark"]/div/xpl-document-details/div/div[1]/section[2]/div/xpl-document-header/section/div[2]/div/div/div[3]/div[2]/div[1]/div[1]/button[{page_btn}]')
        div_elements = button.find_elements(By.XPATH, './div')

        if len(div_elements) >= 2:
            last_div_text = div_elements[-2].text.strip()
            last_div_text_views = div_elements[-1].text.strip()
            concatenated_text = f"{last_div_text} {last_div_text_views}"
            if (concatenated_text in 'Cites in Papers'):
                print('Cites in Papers:', btn_value)
                cites_in_papers = int(btn_value)
            if (concatenated_text in 'Cites in Patent'):
                print('Cites in Patent:', btn_value)
                cites_in_patents = int(btn_value)
            if ('Full' in concatenated_text):
                print('Full Text Views:', btn_value)
                full_text_views = int(btn_value)

    try:
        title = driver.find_element(By.XPATH, '//*[@id="xplMainContentLandmark"]/div/xpl-document-details/div/div[1]/section[2]/div/xpl-document-header/section/div[2]/div/div/div[1]/div/div[1]/h1/span').text
        print('title:', title)
    except:
        title = None

    try:
        page_info = driver.find_element(By.XPATH, '//*[@id="xplMainContentLandmark"]/div/xpl-document-details/div/div[1]/div/div[2]/section/div[2]/div/xpl-document-abstract/section/div[2]/div[3]/div[1]/div[1]/span').text
        pages = int(page_info.split(' ')[-1])
    except:
        pages = None
    print("pages:", pages)

    try:
        publisher = driver.find_element(By.XPATH, '//*[@id="xplMainContentLandmark"]/div/xpl-document-details/div/div[1]/section[2]/div/xpl-document-header/section/div[2]/div/div/div[1]/div/div[1]/div/div[1]/xpl-publisher/span/span/span/span[2]').text
        print("Publisher:", publisher)
    except:
        publisher = None

    try:
        doi = driver.find_element(By.XPATH, '//*[@id="xplMainContentLandmark"]/div/xpl-document-details/div/div[1]/div/div[2]/section/div[2]/div/xpl-document-abstract/section/div[2]/div[3]/div[2]/div[1]/a').text
        print("DOI:", doi)
    except:
        doi = None

    try:
        publication_date_info = driver.find_element(By.XPATH, '//*[@id="xplMainContentLandmark"]/div/xpl-document-details/div/div[1]/div/div[2]/section/div[2]/div/xpl-document-abstract/section/div[2]/div[3]/div[1]/div[1]').text
        publication_date = publication_date_info.split(': ')[-1]
        print("Date of Publication:", publication_date)
    except:
        publication_date = None
        
    try:
        abstract = driver.find_element(By.XPATH, '//*[@id="xplMainContentLandmark"]/div/xpl-document-details/div/div[1]/div/div[2]/section/div[2]/div/xpl-document-abstract/section/div[2]/div[1]/div/div/div').text
        print("Abstract:", abstract)
    except: 
        abstract = None
    
    try:
        published_in = driver.find_element(By.XPATH, '//*[@id="xplMainContentLandmark"]/div/xpl-document-details/div/div[1]/div/div[2]/section/div[2]/div/xpl-document-abstract/section/div[2]/div[2]/a').text
        print("published in:", published_in)
    except:
        published_in = None

    try:
        authors_button = driver.find_element(By.XPATH, '//button[@id="authors"]')
        authors_button.click()
        time.sleep(1)
        authors_info = []
        author_elements = driver.find_elements(By.XPATH, '//div[@class="authors-accordion-container"]/xpl-author-item')
        for author_element in author_elements:
            name_element = (author_element.find_element(By.XPATH, './/a/span').text)
            department_element = (author_element.find_element(By.XPATH, './/div[2]').text)
            author_info = {
            "name": name_element,
            "from": department_element
            }
            authors_info.append(author_info)
            print("Authors:", author_info)
    except:
        authors_info = None

    try:
        keywords_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="keywords-header"]')))
        keywords_button.click()
        time.sleep(1)
        ieeekeywords_section = driver.find_element(By.XPATH, '//*[@id="keywords"]/xpl-document-keyword-list/section/div/ul/li[1]')
        ieeekeywords_elements = ieeekeywords_section.find_elements(By.XPATH, './/li/a')
        ieee_keywords_list = [keyword_element.text.strip() for keyword_element in ieeekeywords_elements]
        print("ieee keywords:", ieee_keywords_list)
    except:
        ieee_keywords_list = None

    try:
        authors_keywords_section = driver.find_element(By.XPATH, '//*[@id="keywords"]/xpl-document-keyword-list/section/div/ul/li[3]')
        authors_keywords_elements = authors_keywords_section.find_elements(By.XPATH, './/li/a')
        authors_keywords_list = [keyword_element.text.strip() for keyword_element in authors_keywords_elements]
        print("authors keywords:", authors_keywords_list)
    except:
        authors_keywords_list = None

    return {
        "title": title,
        "Pages": pages,
        "Cites in Papers": cites_in_papers,
        "Cites in Patent": cites_in_patents,
        "Full Text Views": full_text_views,
        "Publisher": publisher,
        "DOI": doi,
        "Date of Publication": publication_date,
        "abstract": abstract,
        "Published in": published_in,
        "Authors": authors_info,
        "IEEE Keywords": ieee_keywords_list,
        "Author Keywords": authors_keywords_list
    }

articles_info = {
    "Relevance": [],
    "Newest": []
}
page_num = 0
max_pages = 5
ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="xplMainContent"]/div[2]/div[2]/xpl-paginator/div[2]/ul')))
conference_filter = driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div[3]/div/xpl-root/main/div/xpl-search-results/div/div[1]/div[2]/xpl-search-dashboard/section/div/div[1]/xpl-facet-content-type-migr/div/div/div[1]/label/input')
conference_filter.click()
time.sleep(1)
apply_filter = driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div[3]/div/xpl-root/main/div/xpl-search-results/div/div[1]/div[2]/xpl-search-dashboard/section/div/div[1]/xpl-facet-content-type-migr/div/div[2]/button')
apply_filter.click()

while page_num < max_pages:
    WebDriverWait(driver, 12).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="xplMainContent"]/div[2]/div[2]/xpl-paginator/div[2]/ul')))
    articles = driver.find_elements(By.XPATH, '//div[@class="List-results-items"]')

    for i in range(len(articles)):
        article = articles[i]
        article_link = article.find_element(By.XPATH, './/a')
        driver.execute_script("arguments[0].click();", article_link)
        time.sleep(1)
        info = get_article_info()
        articles_info["Relevance"].append(info)
        driver.back()
        driver.back()
        driver.back()
        WebDriverWait(driver, 10, ignored_exceptions=ignored_exceptions).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="xplMainContent"]/div[2]/div[2]/xpl-paginator/div[2]/ul')))
        articles = driver.find_elements(By.XPATH, '//div[@class="List-results-items"]')

    next_button = driver.find_element(By.XPATH, '//*[@id="xplMainContent"]/div[2]/div[2]/xpl-paginator/div[2]/ul/li[11]/button')
    driver.execute_script("arguments[0].click();", next_button)
    page_num += 1

WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="xplMainContent"]/div[2]/div[2]/xpl-paginator/div[2]/ul')))
sort_btn = driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div[3]/div/xpl-root/main/div/xpl-search-results/div/div[2]/div[2]/xpl-results-list/div[2]/xpl-select-dropdown/div/button')
driver.execute_script("arguments[0].click();", sort_btn)

newest_btn = driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div[3]/div/xpl-root/main/div/xpl-search-results/div/div[2]/div[2]/xpl-results-list/div[2]/xpl-select-dropdown/div/div/button[2]')
driver.execute_script("arguments[0].click();", newest_btn)

page_num = 0

while page_num < max_pages:
    WebDriverWait(driver, 12).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="xplMainContent"]/div[2]/div[2]/xpl-paginator/div[2]/ul')))
    articles = driver.find_elements(By.XPATH, '//div[@class="List-results-items"]')

    for i in range(len(articles)):
        article = articles[i]
        article_link = article.find_element(By.XPATH, './/a')
        driver.execute_script("arguments[0].click();", article_link)
        time.sleep(1)
        info = get_article_info()
        articles_info["Newest"].append(info)
        driver.back()
        driver.back()
        driver.back()
        WebDriverWait(driver, 10, ignored_exceptions=ignored_exceptions).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="xplMainContent"]/div[2]/div[2]/xpl-paginator/div[2]/ul')))
        articles = driver.find_elements(By.XPATH, '//div[@class="List-results-items"]')

    next_button = driver.find_element(By.XPATH, '//*[@id="xplMainContent"]/div[2]/div[2]/xpl-paginator/div[2]/ul/li[11]/button')
    driver.execute_script("arguments[0].click();", next_button)
    page_num += 1

with open('articles_info.json', 'w') as f:
    json.dump(articles_info, f, indent=4)

driver.quit()
