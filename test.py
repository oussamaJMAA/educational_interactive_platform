# # import openai
# # openai.api_key = "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"
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

# import openai
# import requests

# def generate_image_from_text(text):
#     openai.api_key = "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"
#     response = openai.Completion.create(
#     model="text-davinci-003",
#     prompt="Translate this into english : "+text+"\n1.",
#     temperature=0.3,
#     max_tokens=100,
#     top_p=1.0,
#     frequency_penalty=0.0,
#     presence_penalty=0.0
#     )
#     return response.choices[0].text
# print(generate_image_from_text("يفيد لديه 13 بالونًا ، إيمي لديها 7 بالونات ، كم عدد البالونات التي يمتلكها ديفيد أكثر من إيمي"))
# print(generate_image_from_text("saly has 4 apples , she gave her sister 2 apples , how many apples Saly has now ?"))


import openai


def grammar_correction(text):
    openai.api_key = "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"
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt="Correct this to standard English: "+text+"\n1.",
    temperature=0,
    max_tokens=60,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0
    )
    return response.choices[0].text
print(grammar_correction("4 groups of children go on (1 school trip.There are 10 children in each group.How many children go on the trip?"))