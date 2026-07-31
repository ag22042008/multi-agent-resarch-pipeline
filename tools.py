from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os 
from rich import print
from dotenv import load_dotenv
load_dotenv()
tavily=TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
@tool
def web_search(query:str)->str:
    "Search the web for recent and reliable information on a topic.Returns titles,urls and snippets"
    results=tavily.search(query=query,max_results=5,search_depth="advanced")
    out=[]
    for r in results['results']:
        out.append(
            f"Title:{r['title']}\n URL:{r['url']}\nSnippet:{r['content'][:500]}\n"
        )
    return "\n---\n".join(out)

@tool #beautifulsoup
def scrape_url(url:str)->str:
    "Scrape and return clean text content from a given URL for deep reading"
    try:
        resp=requests.get(url,timeout=12,headers={"User-Agent":"Mozilla/5.0"})
        # headers to pretend that actual user is giving the request
        soup=BeautifulSoup(resp.text,"html.parser")
        # resp.text (The First Parameter)What it is: This is the raw HTML content of a webpage returned as a text string. Usually, you get this by using Python's requests library to fetch a page (resp = requests.get(url)), and .text extracts the actual HTML markup.Why it is required: BeautifulSoup does not go out to the internet to download webpages on its own. It cannot process a URL directly; it needs the actual raw HTML text handed to it so it can begin reading and analyzing the code.
        #2. "html.parser" (The Second Parameter)What it is: This specifies the parser engine BeautifulSoup should use to read the text. "html.parser" is the built-in HTML parser that comes standard with Python.
        for tag in soup(["script","style","nav","footer"]):# the tags which the soup needs to scrap to provide a good parsed text
            tag.decompose()# remove all these tags
        return soup.get_text(separator=" ",strip=True)[:4000]# extract max 3000 words parsed text to less burn the tokens of mistral api
    except Exception as e:
        return f"Could not scrape Url:{str(e)}"
