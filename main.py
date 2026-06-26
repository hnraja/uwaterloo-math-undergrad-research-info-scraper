import time
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Start driver
options = Options()
options.add_argument("--headless=new")
driver = webdriver.Edge()
driver.get("https://uwaterloo.ca/statistics-and-actuarial-science/research/research-strengths")

# Loop over research strengths 
cards = driver.find_elements(By.CSS_SELECTOR, 
    ".uw-contained-width.uw-section-spacing--default.uw-section-separator--none.uw-column-separator--none.layout.layout--uw-2-col.even-split")

strength_df = pd.DataFrame(columns=['strength', 'desc', 'faculty', 'topic'])

prof_df = pd.DataFrame(columns=['prof', 'link', 'about', 'pubs'])

for c in cards:
    s, desc = c.find_element(By.CLASS_NAME, "uw-copy-text__wrapper").text.strip().split("\n")
    s = s.strip(); desc = desc.strip()
    faculty = c.find_elements(By.TAG_NAME, "li")
    
    # Loop over professors, extracting information from profile pages
    for f in faculty:
        prof, topic = f.text.strip().split(":")
        prof = prof.strip(); desc = desc.strip()
        link = f.find_element(By.TAG_NAME, 'a').get_attribute("href")
        
        strength_df.loc[len(strength_df)] = [s, desc, prof, topic]
        
        if len(prof_df[prof_df['prof'] == prof]) == 0:
            driver.get(link)
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "uw-site-container"))
                )
            except:
                print(f'unable to navigate profile page of {prof}')
                
            new_page_link = str(driver.current_url)                
            prof_df.loc[len(prof_df)] = [prof, new_page_link, "12", "12"]

            driver.back()

driver.quit()
print(prof_df)
# prof_df.to_csv('prof.csv', index=False)

print("☆*: .｡. o(≧▽≦)o .｡.:*☆")

