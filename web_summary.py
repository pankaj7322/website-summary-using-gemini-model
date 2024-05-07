# Importing necessary modules
import os
import google
import google.generativeai as genai
import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
from selenium.webdriver.chrome.options import Options
import re
import time




def extract_website_data(url):

    # create chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    # WebDriver Chrome
    driver = webdriver.Chrome(options=chrome_options)

    # Target URL
    driver.get(url)
    # # To load entire webpage
    time.sleep(1)

    # Getting only the visible text on the website
    visible_text = driver.find_element(By.TAG_NAME, "body").text
    return visible_text

    # Closing the driver
    driver.close()

def generativeai_model(prompt, visible_text):
# accessing google api model
    api_key = "AIzaSyDfzdWQ9YonIv-5qkBXVO0jhS7bCMjd8xo"
    genai.configure(api_key = api_key)

    model = genai.GenerativeModel('gemini-pro')

    # prompt = '''
    #     create the summary from the given contents
    # '''

    response = model.generate_content([prompt, visible_text])
    return response.text



# extract name of the website

def extract_name(url):
    parsed_url = urlparse(url)
    website_name = parsed_url.netloc.split('.')[1]
    return website_name


# create the list
selectboxlist = []

# create the ui
def main():

    # main document
    st.header('Website Summary')
    
    # sidebar
    url = st.sidebar.text_input("Enter the Website Link")
    prompt_text = f''' 
                    Give the summary about the website 

                    Generate the keywords related to it.
                '''

    # add the website name
    

    btn = st.sidebar.button("submit")
    
    # when button press
    if btn:
        selectboxlist.append(extract_name(url))
        st.sidebar.selectbox('select the website', selectboxlist)            

        visible_text = extract_website_data(url)
        # display summary data

        response_new = generativeai_model(prompt_text, visible_text)
        
        summary_text, keywords_text = response_new.split("Keywords")

       

        # Extracting the keywords from the keywords text
        keywords_list = re.findall(r'\* (.+)', keywords_text)
        # st.write(keywords_list)

        # # Displaying the keywords
        text = " , ".join(keywords_list)
        st.write(text)

        

        

        # Displaying the summary
        st.write(summary_text.strip())

        
    


if __name__ == '__main__':
    main()
