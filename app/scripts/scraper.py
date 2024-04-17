import requests
import bs4
from termcolor import colored
from app.database.db_query import DBQuery

class Scraper:
  @staticmethod
  def scrap_all_drugs():
    nb_parsed = 0 
    DBQuery.create_drugs_table()
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    base_url = f"{Scraper.__get_base_url()}/drugs/2/alpha"
    for letter in alphabet:
      url = f"{base_url}/{letter}/"
      for second_letter in alphabet:
        final_url = url + letter + second_letter
        
        headers = Scraper.__get_headers()
        response = requests.get(final_url, headers=headers)
        soup = bs4.BeautifulSoup(response.content, 'html.parser')
        drugs_html = soup.find_all("div", class_="drugs-search-list-conditions")
        
        for drug_html in drugs_html:
          drug = {}
          for drug_name in drug_html.find_all("a"):
            drug['name'] = drug_name.text
            
            if len(DBQuery.get_by_column('name', drug['name'])) > 0:
              print(colored(f"[SKIPPED] {drug['name']}", "yellow"))
              continue
            
            drug['details_url'] = drug_name['href']
            drug = Scraper.scrap_drug(drug)
            
            DBQuery.insert(drug, 'drugs')
            print(colored(f"[INSERTED] {drug['name']}", "green"))
            nb_parsed += 1

        url = url
    print(colored(f"----------\nScraped {nb_parsed} drugs\n----------", "green"))    
    
    
  @staticmethod
  def scrap_drug(drug):
    headers = Scraper.__get_headers()
    response = requests.get(Scraper.__get_base_url() + drug['details_url'], headers=headers)
    soup = bs4.BeautifulSoup(response.content, 'html.parser')
    
    sections = ["uses", "side-effects", "warnings", "precautions", "interactions", "overdose"]
    for section in sections:
      drug[section.replace('-', "_")] = Scraper.__get_content(soup, section)
    
    return drug
  
  @staticmethod
  def __get_content(soup, section):
    content = soup.find("div", class_=f"{section}-container")
    content_text = ""
    
    if content is None:
      return None
 
    tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span']
    content = content.find_all(tags)
    
    for paragraph in content:
      content_text += f"{paragraph.text}\n"
      
    return content_text
  
    content
  @staticmethod
  def __get_headers():
    return {
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
  
  @staticmethod
  def __get_base_url():
    return "https://www.webmd.com"