import time
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os

def scrape():
    # Start driver
    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Edge()
    driver.get("https://uwaterloo.ca/statistics-and-actuarial-science/research/research-strengths")

    # Loop over research strengths 
    cards = driver.find_elements(By.CSS_SELECTOR, 
        ".uw-contained-width.uw-section-spacing--default.uw-section-separator--none.uw-column-separator--none.layout.layout--uw-2-col.even-split")

    strength_df = pd.DataFrame(columns=['strength', 'desc', 'faculty', 'topic'])

    prof_df = pd.DataFrame(columns=['prof', 'link', 'pubs'])

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
                    WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "uw-site-container"))
                    )
                    profile = driver.find_element(By.CLASS_NAME, 'uw-copy-text__wrapper')
                    pubs = [li.text.strip() for li in profile.find_elements(By.TAG_NAME, 'li')]
                except: pubs = []
                    
                new_page_link = str(driver.current_url)
                if len(pubs) == 0:
                    print(f'unable to navigate profile page of {prof}')
                    prof_df.loc[len(prof_df)] = [prof, new_page_link, pd.NA]
                for paper in pubs:
                    prof_df.loc[len(prof_df)] = [prof, new_page_link, paper]
                driver.back()

    driver.quit()
    written = False
    
    file = 'output.xlsx'
    while os.path.isfile(file):
        overwrite = input(f"File {file} already exists. Do you want to overwrite? (Y/N): ")
        if overwrite.lower() == 'y': break
        elif overwrite.lower() == 'n':
            new_name = input('Enter new file name: ').strip()
            if not new_name.endswith('.xlsx'): new_name += '.xlsx'
            file = new_name
        else: print("Invalid argument.")
    
    while not written:
        try:
            with pd.ExcelWriter(file) as writer:
                strength_df.to_excel(writer, sheet_name="Strengths", index=False)
                prof_df.to_excel(writer, sheet_name="Papers", index=False)
            written = True

        except PermissionError:
            closed = input("Cannot save while excel file is still open. Close the file and press enter to continue.")

# scrape()

print("☆*: .｡. o(≧▽≦)o .｡.:*☆")

