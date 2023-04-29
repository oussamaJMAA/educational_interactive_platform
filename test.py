import openai
openai.api_key = "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"
def get_result_of_answer(question,answer):
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt="Translate this into english : "+question+"\n1",
    temperature=0.3,
    max_tokens=100,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0
    )
    response.choices[0].text
    response2 = openai.Completion.create(
    model="text-davinci-003",
    prompt="give me the answer of this by just a number : "+response.choices[0].text,
    temperature=0.3,
    max_tokens=100,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0
    )
    response2.choices[0].text
    rep = response2.choices[0].text.replace('\n','')
    print("true answer:",rep)
    if rep == answer:
        return (True,rep)
    else:
        return (False,rep)
print(get_result_of_answer("If you have 3 cookies and you eat one cookie, how many cookies do you have left?","2")[0])