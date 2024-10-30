import requests
from bs4 import BeautifulSoup

def scrape_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    content = ""
    for para in soup.find_all(['p', 'h2', 'h3']):
        content += para.get_text(separator=" ", strip=True) + "\n"
    return content

def scrape_bedrock_api_docs():
    urls = [
        "https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html"
    ]
    all_content = ""
    for url in urls:
        all_content += scrape_page(url) + "\n"
    return all_content