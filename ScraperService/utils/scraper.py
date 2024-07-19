from time import sleep

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import NoSuchElementException

from API_GATEWAY import BASE_URL
from utils.helpers import get_simple_post_max_tag, get_all_simple_posts


def cpu_bound_func_scrape(user, token, url, scroll, email="ricardobayonalatorre@yahoo.com", password="MiaGordo5"):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--verbose")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument(f"--user-data-dir=login_data")
    # chrome_options.add_experimental_option("detach", True)
    # Initialize Chrome WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    token = token
    user = user

    sleep(1)

    email = email
    password = password

    if email and password:
        login(driver, email, password)

    sleep(2)

    driver.get(url)
    sleep(1)
    driver.refresh()
    sleep(1)

    page = driver.page_source
    soup = BeautifulSoup(page, 'lxml')

    if soup is None:
        print(f"Couldn't load the Page: {url}")
        return []
    tag = get_simple_post_max_tag(soup)

    scroll_(driver, scroll)

    simple_posts = get_all_simple_posts(soup, tag)

    for _ in simple_posts:
        print(_.link)

    driver.quit()

    for simple_post in simple_posts:
        request_NLP_scrape(token, user, simple_post)
        sleep(4)


def login(driver, usr, pwd):
    driver.get('https://www.facebook.com/')
    print("Opened facebook")
    sleep(1)

    try:
        email = driver.find_element('id', 'email')
        email.click()

    except NoSuchElementException:
        print("User is authenticated")
        return

    username_box = driver.find_element('id', 'email')
    username_box.send_keys(usr)
    print("Email Id entered")
    sleep(1)

    password_box = driver.find_element('id', 'pass')
    password_box.send_keys(pwd)
    print("Password entered")

    try:
        login_box = driver.find_element('name', "login")
        login_box.click()
    except Exception as e:

        try:
            login_box = driver.find_element('id', 'u_0_9_PN')
            login_box.click()

        except Exception as e:
            try:
                login_box = driver.find_element('id', "loginbutton")
                login_box.click()
            except Exception as e:
                print(f"Login button not found: {e.__traceback__}")
                pass

    print("Done")


def request_NLP_scrape(token, user, simple_post):
    url = f"{BASE_URL}/scrape-nlp/scrape-nlp/{simple_post.link}"
    headers = {
        "X-Consumer-Custom-Id": user,
        "Authorization": f"Bearer {token['token']}",
    }
    # Make the GET request
    response = requests.post(url, headers=headers)
    # Check the response
    if response.status_code in [200, 201, 202]:
        print("Request was successful")
        print("Response data:", response.json())  # Or response.text for plain text response
    else:
        print(f"Request failed with status code {response.status_code}")
        print("Response data:", response.text)


def scroll_(driver, n):
    for i in range(1, n):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(1.8)


def main():
    url = 'https://www.facebook.com/marketplace/108610652496213/vehicles?maxPrice=4000&maxMileage=200000&minYear=2007&carType=suv&transmissionType=automatic&exact=false'
    username = "ricardobayonalatorre@yahoo.com"
    password = "MiaGordo5"


if __name__ == "__main__":
    main()
