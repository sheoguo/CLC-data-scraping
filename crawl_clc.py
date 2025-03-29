import requests
from bs4 import BeautifulSoup
import json

# Function to get HTML content of a URL
def get_html(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

# Function to parse category page
def parse_category_page(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    categories = []
    for category in soup.select('.category-list .category'):
        code = category.select_one('.category-code').text.strip()
        description = category.select_one('.category-description').text.strip()
        subcategory_link = category.select_one('a.subcategory-link')
        subcategories = []
        if subcategory_link:
            subcategory_url = subcategory_link['href']
            subcategories = parse_category_page(subcategory_url)
        categories.append({
            'code': code,
            'description': description,
            'subcategories': subcategories
        })
    return categories

# Function to parse the main category page
def parse_main_page(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    categories = []
    for main_category in soup.select('.main-category-list .main-category'):
        code = main_category.select_one('.main-category-code').text.strip()
        description = main_category.select_one('.main-category-description').text.strip()
        subcategory_link = main_category.select_one('a.subcategory-link')
        subcategories = []
        if subcategory_link:
            subcategory_url = subcategory_link['href']
            subcategories = parse_category_page(subcategory_url)
        categories.append({
            'code': code,
            'description': description,
            'subcategories': subcategories
        })
    return categories

# Main URL of the categories
main_url = 'https://www.clcindex.com/category/'
categories = parse_main_page(main_url)

# Save the result to a JSON file
with open('categories.json', 'w', encoding='utf-8') as f:
    json.dump(categories, f, ensure_ascii=False, indent=4)

print('Categories have been saved to categories.json')
