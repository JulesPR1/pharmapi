import requests
import bs4
from termcolor import colored
from app.database.db_query import DBQuery

class Scraper:
  @staticmethod
  def scrap_all_drugs():
    DBQuery.clean_table('drugs')
    
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
            drug['details_url'] = drug_name['href']
            drug = Scraper.scrap_drug(drug)
            
            DBQuery.insert(drug, 'drugs')
            print(colored("Inserted: ", drug['name'], "green"))

        url = url
    
  @staticmethod
  def scrap_drug(drug):
    headers = Scraper.__get_headers()
    response = requests.get(Scraper.__get_base_url() + drug['details_url'], headers=headers)
    soup = bs4.BeautifulSoup(response.content, 'html.parser')
    
    drug['uses'] = Scraper.__get_uses(soup)
    # drug['side_effects'] = Scraper.__get_side_effects(soup)
    # drug['precautions'] = Scraper.__get_precautions(soup)
    # drug['interactions'] = Scraper.__get_interactions(soup)
    # drug['overdose'] = Scraper.__get_overdose(soup)
    
    return drug
  
  @staticmethod
  def __get_uses(soup):
    
    intro = soup.find("div", class_="monograph-content")
    how_to_use_paragraphes = soup.find("div", class_="how-to-use-section")
    
    if intro is None:
      return None
    
    how_to_use = ""
    for paragraph in intro.find_all("p"):
      how_to_use += f"\n{paragraph.text}"
    
    if how_to_use_paragraphes is not None:
      how_to_use_paragraphes.find_all("p")
      
      for paragraph in how_to_use_paragraphes:
        how_to_use += f"\n{paragraph.text}"
      
    return how_to_use
    
  @staticmethod
  def __get_headers():
    return {
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
  
  @staticmethod
  def __get_base_url():
    return "https://www.webmd.com"

Scraper.scrap_all_drugs()