import re

import html2text
import requests
from bs4 import BeautifulSoup

from util.document import Document

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    # Add any other headers you want to include
}


def get_all_links(index):
    # Send a GET request to the webpage you want to scrape
    url = f"https://www.webmd.com/diet/medical-reference/default.htm?pg={index}"
    response = requests.get(url, headers=headers)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the ul element with class 'az-index-results-group-list'
    ul_element = soup.find('section', class_='dynamic-index-feed').find('ul', class_='list')

    # Find all the links (a tags) within the ul element
    links = ul_element.find_all('a')

    # Extract the href attribute from each link
    all_links = [link['href'] for link in links]

    return all_links


def split_markdown_by_headings(markdown_text):
    # Define the regular expression pattern to match H1 and H2 headings
    pattern = r'(#{1,2}.*)'

    # Split the Markdown text based on the headings
    sections = re.split(pattern, markdown_text)

    # Combine each heading with its corresponding text
    combined_sections = []
    for i in range(1, len(sections), 2):
        heading = sections[i].strip()  # Get the heading from sections[i]
        text = sections[i + 1].strip() if i + 1 < len(
            sections) else ''  # Get the text from sections[i + 1] if it exists, otherwise use an empty string
        combined_section = f"{heading}\n{text}"  # Combine the heading and text using a newline character
        combined_sections.append(combined_section)  # Add the combined section to the list

    if len(combined_sections) == 0:
        combined_sections = [markdown_text]

    return combined_sections


processed_links = []


def scrape_webpage(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    try:
        title = soup.find('h1').get_text().strip()

        article_body = soup.find(class_='article__body')
        if article_body is None:
            article_body = soup.find(class_='article-body')
        html_content = str(article_body)
        markdown_content = html2text.html2text(html_content, bodywidth=0)

        link_pattern = re.compile(r'\[(.*?)\]\((.*?)\)')
        matches = link_pattern.findall(markdown_content)
        for _match in matches:
            full_match = f'[{_match[0]}]({_match[1]})'
            markdown_content = markdown_content.replace(full_match, _match[0])

        content = split_markdown_by_headings(markdown_content)
        docs = []
        for _content in content:
            docs.append(Document(title=title, url=url, content=_content))
        return docs
    except:
        return []
