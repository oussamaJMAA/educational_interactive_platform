# # import openai
# # openai.api_key = "api_key"
# # def get_result_of_answer(question,answer):
# #     response = openai.Completion.create(
# #     model="text-davinci-003",
# #     prompt="Translate this into english : "+question+"\n1",
# #     temperature=0.3,
# #     max_tokens=100,
# #     top_p=1.0,
# #     frequency_penalty=0.0,
# #     presence_penalty=0.0
# #     )
# #     response.choices[0].text
# #     response2 = openai.Completion.create(
# #     model="text-davinci-003",
# #     prompt="give me the answer of this by just a number : "+response.choices[0].text,
# #     temperature=0.3,
# #     max_tokens=100,
# #     top_p=1.0,
# #     frequency_penalty=0.0,
# #     presence_penalty=0.0
# #     )
# #     response2.choices[0].text
# #     rep = response2.choices[0].text.replace('\n','')
# #     print("true answer:",rep)
# #     if rep == answer:
# #         return (True,rep)
# #     else:
# #         return (False,rep)
# # print(get_result_of_answer("If you have 3 cookies and you eat one cookie, how many cookies do you have left?","2")[0])     


# import gradio as gr


# # import libraries for selenium
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options 
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time
# import os

# problem_text = "If you have 15 toy cars and you give 8 toy cars to your friend, how many toy cars do you have left?"
# chrome_driver_path = "C:/DsProjects/chromedriver.exe"
# #gr.load("models/oussama120/wp-converter").launch(share=True)

# browser = webdriver.Chrome(executable_path=chrome_driver_path)
# browser.get("http://127.0.0.1:7860")
# wait_textarea = WebDriverWait(browser, 10).until(
#     EC.presence_of_element_located((By.TAG_NAME, "textarea"))
# )
# textarea = browser.find_element(By.TAG_NAME,'textarea')
# textarea.send_keys(problem_text)
# submit_button = browser.find_element(By.XPATH, '//button[text()="Submit"]')
# submit_button.click()
# #wait up to 10 seconds for the element to be clickable
# div_element = WebDriverWait(browser, 55).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[aria-label="Download"]')))
# # click the element
# div_element.click()


import os

download_path = "C:/Users/oussa/Downloads/"
image_name = 'image.jpg'
relative_path = os.path.relpath(download_path + image_name, 'app/templates')
print(relative_path.replace('\\', '/'))
