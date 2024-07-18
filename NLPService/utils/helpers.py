import datetime
import itertools
import os
import re
import shutil
from io import BytesIO

import boto3
import requests
import spacy
from PIL import Image
from botocore.exceptions import NoCredentialsError
from dateutil.relativedelta import relativedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import S3_BUCKET
from DTOs.DetailedPost import DetailedPost
from utils.filter_keywords import *


def get_past_date_from_relative_date(str_days_ago):
    print(str_days_ago)
    today = datetime.date.today()
    split = str_days_ago.split()

    if split[0].lower() == "a" or split[0].lower() == "an" or split[0].lower() == "one":
        split[0] = "1"

    if len(split) == 1 and split[0].lower() == "today":
        return str(today.isoformat())
    elif len(split) == 1 and split[0].lower() == "yesterday":
        return today - relativedelta(days=1)

    elif split[1].lower() in ["hour", "hours", "hr", "hrs", "h"]:
        return datetime.datetime.now() - relativedelta(hours=int(split[0]))

    elif split[1].lower() in ["day", "days", "d"]:
        return today - relativedelta(days=int(split[0]))

    elif split[1].lower() in ["wk", "wks", "week", "weeks", "w"]:
        return today - relativedelta(weeks=int(split[0]))

    elif split[1].lower() in ["mon", "mons", "month", "months", "m"]:
        return today - relativedelta(months=int(split[0]))

    elif split[1].lower() in ["yrs", "yr", "years", "year", "y"]:
        return today - relativedelta(years=int(split[0]))

    elif split[1].lower() in ["min", "mins", "minutes", "minute", "m"]:
        return today - relativedelta(hours=1)
    else:
        return today


def validate(post: DetailedPost):
    is_valid = True

    for ignored in IGNORE:
        search1 = re.search(ignored, post.description, re.IGNORECASE)
        search2 = re.search(ignored, post.scraped_text, re.IGNORECASE)

        if search1 or search2:
            print(search1)
            print(search2)
            is_valid = False
            break

    if post.price < 800:
        print(post.price)
        is_valid = False

    if len(post.images) <= 1:
        print("Not enough images")
        is_valid = False

    print("Post validaiton: ", is_valid)

    if not is_valid:
        raise Exception("Post is not valid")


def get_topn_tags(soup, n):
    tags = soup.find_all(["span", "a", "li", "lu", "img", "h1", "p"])

    classes = {}

    for tag in tags:
        if tag.has_attr("class"):
            cList = tag["class"]
            key = ""
            for c in cList:
                key += " " + c

            if key not in ["", " "]:
                if classes.get(key) is None:
                    classes[key] = 1
                else:
                    classes[key] += 1

    classes = {key[1:]: value for key, value in classes.items() if value >= n}

    print("maxtags")
    print(classes)

    return classes


def clean_post_soup(soup):
    # Find all div tags
    div_tags = soup.find_all("div")

    # Define the strings X and Y
    strings_x = [
        "aboutthisvehicle",
        "seemore",
        "seller'sdescription",
        "sellerinformation",
        "sellerdetails",
    ]
    string_y = "today'spicks"

    # Initialize variables to track minimum depth and corresponding div tag
    min_depth = float("inf")  # Start with an infinitely large number
    min_depth_div = None

    # Iterate through div tags and find the one with minimum depth that meets conditions
    for div in div_tags:
        text = div.get_text()
        text = re.sub(r"\s+", "", text).lower()

        contains_x = False

        for x in strings_x:
            if x in text:
                contains_x = True
                break

        if contains_x and string_y not in text:
            # Calculate depth of current div tag
            current_depth = len(list(div.parents))

            # Update minimum depth and corresponding div tag if current one has lesser depth
            if current_depth < min_depth:
                min_depth = current_depth
                min_depth_div = div

    return min_depth_div


def get_xpath(element):
    components = []

    child = element if element.name else element.parent

    for parent in child.parents:
        previous = itertools.islice(parent.children, 0, parent.contents.index(child))
        xpath_tag = child.name
        xpath_index = sum(1 for i in previous if i.name == xpath_tag) + 1
        components.append(
            xpath_tag if xpath_index == 1 else "%s[%d]" % (xpath_tag, xpath_index)
        )
        child = parent
    components.reverse()

    return "/%s" % "/".join(components)


def extract_date_location(soup):
    NER = spacy.load("en_core_web_sm")
    location_and_time = "1 week ago in USA"
    dic_ents_date = {}

    text_m = ""
    for d in soup:
        text_m += d.get_text("|")

    date_raw = text_m.split("|")

    for i in range(len(date_raw) - 2):
        t = date_raw[i] + " " + date_raw[i + 1] + " " + date_raw[i + 2]
        t = re.sub(" +", " ", t)
        ner = NER(t)
        dic_ents_date[t] = ""

        if len(ner.ents) <= 3:
            for ent in ner.ents:
                dic_ents_date[t] += "-" + ent.label_

        if (
            "TIME" in dic_ents_date[t] or "DATE" in dic_ents_date[t]
        ) and "GPE" in dic_ents_date[t]:
            location_and_time = t
            break

    print(location_and_time, "location_and_time")

    split = location_and_time.split(" in ")

    if len(split) == 2:
        relative_date = split[0]
        location = split[1]
    else:
        relative_date = split[0]
        location = location_and_time

    date = get_past_date_from_relative_date(relative_date)

    return date, location


def extract_model_price_miles_description_and_scraped_text_about_seller(post_soup_m):
    NER = spacy.load("en_core_web_sm")

    attrs, description, dic, scraped_text = extract_desc_scraped_text(NER, post_soup_m)

    scraped_text, sections = extract_sections(scraped_text)

    about_list, seller_list = extrat_about_seller(sections)

    miles_d, model, price_d, year = extract_model_price_miles(NER, attrs, dic)

    return scraped_text, description, miles_d, model, price_d, year, about_list, seller_list


def extract_desc_scraped_text(NER, post_soup_m):
    text_m = ""
    for d in post_soup_m:
        text_m += d.get_text("|")
    text_m = (
        text_m.replace("This listing is far from your current location.", "")
        .replace("See listings near me", "")
        .replace("Send seller a message", "")
        .replace("Is this still available?", "")
        .replace("Hello, is this still available?", "")
        .replace("Report listing", "")
        .replace("Report Seller", "")
        .replace("Send", "")
        .replace("See All", "")
        .replace("·", " ")
    )
    text_m = re.sub(" +", " ", text_m)
    attrs = text_m.split("|")
    description = ""
    scraped_text = ""

    dic = {}
    for x in attrs:
        dic[x] = ""
        ner = NER(x)

        if len(x) > 30:
            description += x + "|\n"

        if len(ner.ents) <= 3 and x != "":
            scraped_text += x + "|\n"

        for ent in ner.ents:
            dic[x] += "-" + ent.label_
    return attrs, description, dic, scraped_text


def extract_sections(scraped_text):
    sections = [
        r"about\s*this\s*vehicle",
        r"seller's\s*description",
        r"seller\s*information",
        r"seller\s*details",
        r"sponsored",
    ]
    for p in sections:
        s_ = r"\s*(" + p + r")\s*"
        pattern = re.compile(s_, re.IGNORECASE)
        scraped_text = pattern.sub(r"{*\1{", scraped_text)
    scraped_text = "{*Main scraped_text{" + scraped_text
    sections = scraped_text.split("{")
    return scraped_text, sections


def extract_model_price_miles(NER, attrs, dic):
    model = ""
    price = ""
    miles = ""
    for attr in attrs:
        if ("DATE" in dic[attr] or "CARDINAL" in dic[attr]) and (
                "ORG" in dic[attr] or "PRODUCT" in dic[attr]
        ):
            model = attr
            break
    for attr in attrs:
        if "MONEY" in dic[attr]:
            price = attr
            break
    for attr in attrs:
        if "QUANTITY" in dic[attr]:
            miles += attr
            break
    print(model)
    print(price)
    print(miles)
    miles_arr = [int(s) for s in miles.replace(",", "").split() if s.isdigit()]
    miles_d = 0
    if len(miles_arr) > 0:
        miles_d = miles_arr[0]
    price_d = float(price.replace("$", "").replace(",", ""))
    ner_model = NER(model)
    year = 0
    for ents in ner_model.ents:
        if (
                ents.label_ == "DATE" or ents.label_ == "CARDINAL"
        ) and ents.text.isnumeric():
            year = int(ents.text)
            break
    return miles_d, model, price_d, year


def extrat_about_seller(sections):
    about_list = []
    seller_list = []
    for index, section in enumerate(sections):
        if section.lower().startswith("*") and index + 1 < len(sections):
            about_pattern = re.compile(r'about\s*this\s*vehicle', re.IGNORECASE)
            seller_pattern1 = re.compile(r"seller's\s*description", re.IGNORECASE)
            seller_pattern2 = re.compile(r"seller\s*information", re.IGNORECASE)
            seller_pattern3 = re.compile(r"seller\s*details", re.IGNORECASE)

            index_ = sections[index + 1].replace("\n", "")
            split = index_.split("|")
            split = [item for item in split if item.strip()]

            if bool(about_pattern.search(section)):
                about_list.extend(split)

            elif bool(seller_pattern1.search(section)) or bool(seller_pattern2.search(section)) or bool(
                    seller_pattern3.search(section)):
                seller_list.extend(split)
    return about_list, seller_list


def extract_images(main_post_m):
    img_clean = []
    imgs = get_images(main_post_m)
    for img_url in imgs:
        if img_url.startswith("https://scontent"):
            img_clean.append(img_url)

    return img_clean


def save_images_to_s3(img_clean, link):
    session = boto3.Session(
        aws_access_key_id=S3_BUCKET.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=S3_BUCKET.AWS_SECRET_ACCESS_KEY,
    )
    s3 = session.resource('s3')

    local_imgs = download_images(img_clean, link)
    s3_imgs = []

    for img in local_imgs:
        try:

            image_name = os.path.basename(img)

            s3.meta.client.upload_file(Filename=img, Bucket=S3_BUCKET.BUCKET_NAME, Key=image_name)

            s3_url = f"https://{S3_BUCKET.BUCKET_NAME}.s3.amazonaws.com/{image_name}"
            s3_imgs.append(s3_url)

            print(f"Successfully uploaded {img} to {s3_url}")

        except FileNotFoundError:
            print(f"The file {img} was not found.")
        except NoCredentialsError:
            print("Credentials not available.")
        except Exception as e:
            print(f"An error occurred: {e}")

    empty_folder("utils/media")

    return s3_imgs


def download_images(img_clean, link):
    local_imgs = []
    for index, img in enumerate(img_clean):
        try:
            # Send a GET request to the image URL
            response = requests.get(img)
            response.raise_for_status()  # Check if the request was successful

            # Open the image using PIL
            image = Image.open(BytesIO(response.content))

            width_percent = 250 / float(image.size[0])
            new_height = int((float(image.size[1]) * float(width_percent)))

            # Resize the image
            image = image.resize((250, new_height))

            # Save the image locally
            image.save(f"utils/media/{link}-{index}.jpg", quality=100)
            local_imgs.append(f"utils/media/{link}-{index}.jpg")
            print(
                f"Image successfully downloaded and saved to {f'media/{link}-{index}.jpg'}"
            )

        except Exception as e:
            print(f"An image error occurred: {e}")
    return local_imgs


def get_images(post_soup):
    img_buttons = post_soup.find_all("div", role="button")
    divs_with_button_and_img = [
        div for div in img_buttons if div.find("img") is not None
    ]

    imgs = []
    for divs in divs_with_button_and_img:
        for element in divs:
            img_tmp = element.find_all("img")
            for img in img_tmp:
                imgs.append(img["src"])

    if len(imgs) < 3:
        raise Exception("Post is not valid: not enough images")

    return imgs


def see_more(driver, soup):
    buttons = [soup.find_all("div", role="button")]

    see_more_list = []

    for set_ in buttons:
        for element in set_:
            if element.text.lower().replace(" ", "") == "seemore":
                see_more_list.append(element)

    for _ in see_more_list:
        xpath = get_xpath(_)

        try:
            element = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            element.click()

            clickable = driver.find_element(By.XPATH, xpath)
            clickable.click()

            driver.execute_script("arguments[0].click();", clickable)

        except Exception as e:
            print(f"Exception occurred for see more: {e}")


def empty_folder(folder_path):
    try:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)  # Remove file
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Remove directory and its contents
        print(f"Folder '{folder_path}' has been emptied.")
    except FileNotFoundError:
        print(f"The folder '{folder_path}' does not exist.")
    except PermissionError:
        print(f"Permission denied to empty '{folder_path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")