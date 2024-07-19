import os
import shutil
import traceback
from time import sleep

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys

import API_GATEWAY
from DTOs.DetailedPost import DetailedPost
from utils.helpers import (
    extract_images,
    clean_post_soup,
    extract_model_price_miles_description_and_scraped_text_about_seller,
    extract_date_location,
    validate,
    save_images_to_s3,
    see_more,
)


def cpu_bound_func_scrape(link_id, user, token):
    delete_folder_if_exists(f"user_login_data/original_data{link_id}")
    shutil.copytree("user_login_data/original_data", f"user_login_data/original_data{link_id}")

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--verbose")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument(f"--user-data-dir=user_login_data/original_data{link_id}")
    # chrome_options.add_experimental_option("detach", True)
    # Initialize Chrome WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get("https://m.facebook.com/marketplace/item/" + link_id)
        sleep(3)

        post_soup = BeautifulSoup(driver.page_source, "lxml")

        sleep(5)

        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

        see_more(driver, post_soup)

        sleep(5)

        post_soup = BeautifulSoup(driver.page_source, "lxml")

        driver.quit()

        imgs_clean = extract_images(post_soup)

        post_soup = clean_post_soup(post_soup)

        if post_soup is None:
            raise f"Couldn't load the Page: {link_id}"

        (
            scraped_text,
            description,
            miles_d,
            model,
            price_d,
            year,
            about,
            seller,

        ) = extract_model_price_miles_description_and_scraped_text_about_seller(post_soup)

        date, location = extract_date_location(post_soup)

        detailed_post = DetailedPost(
            scraped_text,
            description,
            date,
            price_d,
            model,
            location,
            miles_d,
            link_id,
            year,
            imgs_clean,
            about,
            seller,
        )

        validate(detailed_post)

        local_images = save_images_to_s3(imgs_clean, link_id)
        detailed_post.images = local_images

        print(detailed_post)

        publish_to_api(user, link_id, detailed_post, token)

        shutil.rmtree(f"user_login_data/original_data{link_id}")

    except Exception as e:
        shutil.rmtree(f"user_login_data/original_data{link_id}")
        print(link_id, e)
        traceback.print_exc()


def login():

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--verbose")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    chrome_options.add_argument(f"--user-data-dir=user_login_data/original_data")

    # chrome_options.add_experimental_option("detach", True)
    # Initialize Chrome WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    usr = "ricardobayonalatorre@yahoo.com"
    pwd = "MiaGordo5"

    driver.get("https://www.facebook.com/")
    print("Opened facebook")
    sleep(1)

    try:
        email = driver.find_element("id", "email")
        email.click()

    except NoSuchElementException:
        print("User is authenticated")
        return

    username_box = driver.find_element("id", "email")
    username_box.send_keys(usr)
    print("Email Id entered")
    sleep(1)

    password_box = driver.find_element("id", "pass")
    password_box.send_keys(pwd)
    print("Password entered")

    try:
        login_box = driver.find_element("name", "login")
        login_box.click()
    except Exception as e:

        try:
            login_box = driver.find_element("id", "u_0_9_PN")
            login_box.click()

        except Exception as e:
            try:
                login_box = driver.find_element("id", "loginbutton")
                login_box.click()
            except Exception as e:
                raise f"Login button not found: {e.__traceback__}"

    print("Login done")
    sleep(2)
    driver.get("https://www.facebook.com/")
    sleep(1)


def publish_to_api(user_id, scraped_id, post: DetailedPost, token):
    try:
        # Define the endpoint URL
        url = f"{API_GATEWAY.BASE_URL}/create/"
        headers = {
            'Authorization': token['token'],
            'X-Consumer-Custom-Id': user_id,
        }

        print(headers)
        print(f"Posting car '{scraped_id}' to user '{user_id}'...")

        post_data = post.to_dict()

        # Make a POST request
        response = requests.post(url, headers=headers, json=post_data)

        # Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            print(f"Car '{scraped_id}' posted to user '{user_id}' successfully.")
            return True
        else:
            print(f"Failed to post car. Status code: {response.status_code} {response.text}")
            return False

    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return False

def delete_folder_if_exists(folder_path):
    # Check if the folder exists
    if os.path.exists(folder_path):
        print(f"Folder '{folder_path}' exists. Deleting...")
        # Delete the folder and all its contents
        shutil.rmtree(folder_path)
        print(f"Folder '{folder_path}' has been deleted.")
    else:
        print(f"Folder '{folder_path}' does not exist.")


def main():
    cpu_bound_func_scrape("101546652903706")


if __name__ == "__main__":
    main()


