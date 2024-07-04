import requests
from bs4 import BeautifulSoup
import time
import datetime
import pandas as pd
import logging
from src.utils.config import BASE_URL, RECIPE_LIST_URL, HEADERS
import traceback

cur_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
log_file_name = f"../../logs/scraper/scraper_{cur_time}.log"
logging.basicConfig(level=logging.INFO, filename=log_file_name, filemode='w', format='%(asctime)s - %(message)s')

def get_number_of_pages():
    """
    Fetches the total number of pages from the recipe list URL.

    :return:
        int: Total number of pages.
    """
    response = requests.get(RECIPE_LIST_URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the span with class 'page-numbers dots'
    dots_span = soup.find('span', class_='page-numbers dots')
    if dots_span:
        # Find the next 'a' sibling after the dots span
        next_page_link = dots_span.find_next('a', class_='page-numbers')
        if next_page_link:
            total_pages = int(next_page_link.get_text(strip=True))
            return total_pages

    return 1  # Default to 1 if no pagination is found

def get_recipe_links(total_pages):
    """
    Fetches all the recipe links from the recipe list URL

    :return:
        List: List of recipe URLs.
    """
    recipe_links = []
    for page in range(1, total_pages+1):
        # sleeping for 5 seconds to prevent IP blocking
        time.sleep(5)
        page_url = f"{RECIPE_LIST_URL}/page/{page}"
        print(f"{page_url}")
        page_response = requests.get(page_url, headers=HEADERS)
        if page_response.status_code != 200:
            print(f"Failed to fetch page {page}")
            continue

        page_soup = BeautifulSoup(page_response.content, "html.parser")
        articles_container = page_soup.find("div", class_="grid grid-cols-12 gap-4")
        articles = articles_container.find_all("article")
        for article in articles:
            recipe_links.append(article.find("a")["href"])
    return recipe_links


def get_recipes(recipe_url):
    try:
        print(f"Getting recipe details from {recipe_url}")
        recipe_response = requests.get(recipe_url, headers=HEADERS)
        recipe_soup = BeautifulSoup(recipe_response.content, "html.parser")
        recipe_div = recipe_soup.find("div", class_="tasty-recipes")
        recipe_img = recipe_div.find("img", class_="attachment-thumbnail size-thumbnail")["src"]
        recipe_title = recipe_div.find("h2", class_="tasty-recipes-title").text
        recipe_total_time = recipe_div.find("span", class_="tasty-recipes-total-time").text

        try:
            recipe_description = recipe_div.find("div", class_= "tasty-recipes-description-body").find("p").text
        except Exception:
            # Going ahead with empty description
            recipe_description = ""
        recipe_ingredients_sibling = recipe_div.find("div", class_= "tasty-recipes-ingredients-header")
        recipe_ingredients = recipe_ingredients_sibling.findNextSibling("div")
        ingredients = []
        for li_tag in recipe_ingredients.findAll('li'):
            ingredients.append(li_tag.input["aria-label"])

        instructions = []
        recipe_instructions_sibling_div = recipe_div.find("div", class_="tasty-recipes-instructions-header")
        recipe_instructions_div = recipe_instructions_sibling_div.findNextSibling("div")
        instruction_items = recipe_instructions_div.findAll("li")
        for item in instruction_items:
            instructions.append(item.text)

        recipe = {'image': recipe_img,
                  'title': recipe_title,
                  'description': recipe_description,
                  'total time': recipe_total_time,
                  'ingredients': ingredients,
                  'instructions': instructions
                  }
        return recipe
    except Exception as e:
        traceback_info = traceback.format_exc()
        print(f"Exception {e} occurred while scraping {recipe_url}")
        print(f"Traceback info: {traceback_info}")
        return None


def scrape_recipes():
    """
    Scrapes recipes from the website.
    """
    # Get total number of pages
    total_pages = get_number_of_pages()
    print(f'Total number of pages to scrape: {total_pages}')
    # Get links of all recipes from all pages
    recipe_urls = get_recipe_links(total_pages)
    for recipe_url in recipe_urls:
        logging.info(f"Started scraping {recipe_url}")
        time.sleep(120)
        recipe_data = get_recipes(recipe_url)
        if recipe_data:
            print(recipe_data)
            logging.info(f"Completed scraping {recipe_url}")
            save_recipe_to_csv(recipe_data)
        else:
            logging.error(f"Failed to scrape {recipe_url}")


def save_recipe_to_csv(recipe, filename='../../data/raw/recipes.csv'):
    df = pd.DataFrame([recipe])
    print(df.head(10))
    try:
        df.to_csv(filename, mode='a', header=not pd.io.common.file_exists(filename), index=False)
    except PermissionError:
        logging.error(f"Permission denied for file {filename}")
    except OSError as e:
        logging.error(f"Error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error occurred: {e}")

if __name__ == "__main__":
    # Scrape recipes
    scrape_recipes()
