from flask import render_template, request, redirect, url_for, flash, session
from app.forms import RegistrationForm, LoginForm
import aiohttp
from io import BytesIO
from PIL import Image
import asyncio
import base64
import pytesseract
import pickle
import shutil

# import libraries for selenium
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
from app.models import User, Question, Feedback , Answer
from app import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import os
import openai
import base64
import requests
import gradio as gr
from langdetect import detect
openai.api_key = "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"
import random

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
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
def give_hint_to_question(question):
    openai.api_key = "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"
    response2 = openai.Completion.create(
  model="text-davinci-003",
  prompt="explain this to a kid with math operations if needed without giving the answer : "+question,
  temperature=0.3,
  max_tokens=100,
  top_p=1.0,
  frequency_penalty=0.0,
  presence_penalty=0.0
)
    response2.choices[0].text
    rep = response2.choices[0].text.replace('\n','')
    return rep

def is_english(text):
    return detect(text) == 'en'

def translate_to_english(text):
    if is_english(text):
        return text
    else:
        openai.api_key = "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"
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt="Translate this into english : "+text+"\n1.",
            temperature=0.3,
            max_tokens=100,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        return response.choices[0].text

def download_image(problem_text):
    #chrome_options = Options()
    #chrome_options.add_argument("--headless")
    #chrome_driver_path = "C:/DsProjects/chromedriver.exe"
    # browser = webdriver.Chrome(executable_path=chrome_driver_path,options=chrome_options)
    #browser = webdriver.Chrome(executable_path=chrome_driver_path)
    options = Options()
    options.headless = True

    # Optional: set Firefox preferences
    fp = webdriver.FirefoxProfile()
    fp.set_preference('browser.download.folderList', 2)
    fp.set_preference('browser.download.manager.showWhenStarting', False)
    fp.set_preference('browser.download.dir', 'C:/Users/oussa/Downloads')
    fp.set_preference('browser.helperApps.neverAsk.saveToDisk', 'image/jpeg')

    # Optional: specify path to Firefox binary
    firefox_binary_path = 'C:/Program Files/Mozilla Firefox/firefox.exe'
    options.binary_location = firefox_binary_path

    driver_path = 'C:/Users/oussa/Downloads/geckodriver-v0.33.0-win32/geckodriver.exe'
    browser = Firefox(options=options, firefox_profile=fp, executable_path=driver_path)
    browser.get("http://127.0.0.1:7860")
    wait_textarea = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "textarea"))
    )
    textarea = browser.find_element(By.TAG_NAME, "textarea")
    textarea.send_keys(problem_text)
    submit_button = browser.find_element(By.XPATH, '//button[text()="Submit"]')
    submit_button.click()
    # wait up to 10 seconds for the element to be clickable
    div_element = WebDriverWait(browser, 100).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'button[aria-label="Download"]')
        )
    )
    # click the element
    div_element.click()
    time.sleep(5)
    browser.quit()
    # renaming image
    ############################################
    os.chdir("C:/Users/oussa/Downloads/")
    # Get a list of all files in the directory
    files = os.listdir()

    # Filter for image files (e.g., .jpg, .png, etc.)
    image_files = [
        file for file in files if file.endswith(".jpg")
    ]

    # Sort the image files by creation time (newest to oldest)
    image_files.sort(key=os.path.getctime, reverse=True)
    # get 3 random number and characters concatenated
    random_number = random.randint(100, 99999)
    random_char = random.sample("abcdefghijklmnopqrstuvwxyz", 4)
    print(random_char)
    # concatenate the random number and character
    random_number_char = str(random_number) + "".join(random_char)
    # Rename the last image file to a new name
    new_name = f"image {random_number_char}.jpg"  # Replace with your desired new name
    os.rename(image_files[0], new_name)
    ############################################
    # Source file path
    src_path = f"C:/Users/oussa/Downloads/{new_name}"

    # Destination file path
    dst_path = (
        r"C:\Users\oussa\Desktop\Educational_interactive_platform\app\static\uploads"
    )

    # Copy the file from source to destination
    shutil.copy(src_path, dst_path)

    return f"image {random_number_char}.jpg"


def has_answered_question(user_id):
    answers = Answer.query.filter_by(user_id=user_id).all()
    return len(answers) > 0
@app.route("/")
def home():
    #check if the user has answered a question
    if current_user.is_authenticated:
        if  has_answered_question(current_user.id)==False:
            last_10_questions = Question.query.filter_by(user_id=current_user.id).order_by(Question.id.desc()).limit(5).all()
            questions_to_predict = [question.question_text for question in last_10_questions]
            print(questions_to_predict)
            #load the model
            with open(r"C:\Users\oussa\Desktop\Educational_interactive_platform\app\static\models\finalized_model.sav","rb",) as f:
                model = pickle.load(f)
            #load the vectorizer
            with open(r"C:\Users\oussa\Desktop\Educational_interactive_platform\app\static\models\vectorizer.pickle","rb",) as f:
                vectorizer = pickle.load(f)
            #predict the level for each element in the list of questions
            max_level = 0
            for question in questions_to_predict:
                predictions = model.predict(vectorizer.transform([question]))
                # Update the max_output if the current output is greater than it
                if predictions > max_level:
                    max_level = predictions

            #get the level name
            if max_level == 0:
                level_name = "Easy"
            elif max_level == 1:
                level_name = "Medium"
            else:
                level_name = "Hard"
            # give the user that level
            current_user.level = level_name
            db.session.commit()

            
            
       
    return render_template("home.html", title="Home_Page")


def extract_text(img_path):
    im = Image.open(img_path)
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Users\oussa\AppData\Local\Tesseract-OCR\tesseract.exe"
    )
    text = pytesseract.image_to_string(im, lang="eng")
    return text


@app.route("/about", methods=["GET", "POST"])
@login_required
def about():
    if request.method == "POST":
        if "problem_image" in request.files:
            file = request.files["problem_image"]
            if file:
                # Save the uploaded file to a temporary location
                filepath = "C:/Users/oussa/Desktop/Educational_interactive_platform/problem_image.png"
                file.save(filepath)

                # Extract the text from the image using OCR
                pytesseract.pytesseract.tesseract_cmd = (
                    r"C:\Users\oussa\AppData\Local\Tesseract-OCR\tesseract.exe"
                )
                problem_text = pytesseract.image_to_string(Image.open(filepath))
                problem_text = grammar_correction(problem_text)
                # generate_image(problem_text)
                # If an image was uploaded, render the template with problem_text
                return render_template("about.html", problem_text=problem_text)

        # If no image was uploaded, use the text input field value instead

        problem_text = request.form.get("text")
        problem_text = translate_to_english(problem_text)
        question = Question(question_text=problem_text, user_id=current_user.id)
        db.session.add(question)
        db.session.commit()
        # img_url=generate_image2(problem_text)
        # Generate the math problem image and return it to the user
        # img_url = generate_image2(problem_text)
        img_url = download_image(problem_text)
        print("img_url", img_url)
        print("problem", problem_text)
        hint = give_hint_to_question(problem_text)

        # Render the template with img_url
        return render_template("about.html", img_url=img_url, problem_text=problem_text,hint=hint)

    is_correct = request.args.get("is_correct")
    answer_text = request.args.get("answer_text")
    img_url = request.args.get("img_url1")
    correct_answer = request.args.get("correct_answer")
    p = request.args.get("problem_text")
    print(f"answer_text: {answer_text}")
    print(f"is_correct: {is_correct}")
    print(f"correct_answer: {correct_answer}")
    print(f"img_url: {img_url}")

    if img_url:

        return render_template(
            "about.html",
            img_url=img_url,
            problem_text=request.form.get("problem_text"),
            answer_text=answer_text,
            is_correct=is_correct,
            correct_answer=correct_answer,
            p=p,
        )

    # Render the template without img_url or answer section
    return render_template(
        "about.html", problem_text="", is_correct=is_correct, answer_text="", img_url=""
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            username=form.username.data, email=form.email.data, password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        # if form is valid, then flash a success message
        flash(f"Account created for {form.username.data}!", "success")
        # redirect to the home page
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    # if form is valid, then flash a success message
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Login Unsuccessful. Please check email and password", "danger")

    return render_template("login.html", title="Login", form=form)


def check_if_answer_is_correct(question, answer):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Translate this into english : " + question + "\n1",
        temperature=0.3,
        max_tokens=100,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )
    response.choices[0].text
    response2 = openai.Completion.create(
        model="text-davinci-003",
        prompt="give me the answer of this by just a number : "
        + response.choices[0].text,
        temperature=0.3,
        max_tokens=100,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )
    response2.choices[0].text
    rep = response2.choices[0].text.replace("\n", "")
    if rep == answer:
        return (True, rep)
    else:
        return (False, rep)


@app.route("/answer", methods=["POST"])
def check_answer():
    user = current_user
    curr_level = user.level
    answer_text = request.form.get("answer")
    question = request.form.get("problem_text")
    is_correct = check_if_answer_is_correct(question, answer_text)[0]
    correct_answer = check_if_answer_is_correct(question, answer_text)[1]
    user.add_answer(answer_text, is_correct)
    user.nb_attempts += 1
    db.session.commit()
    if user.nb_attempts == 3:
        level = user.get_level(curr_level)
        user.level = level
        user.nb_attempts = 0
        db.session.commit()
    img_url = request.form.get("img_url1")
    print(img_url)
    return redirect(
        url_for(
            "about",
            is_correct=is_correct,
            answer_text=answer_text,
            img_url1=img_url,
            correct_answer=correct_answer,
            problem_text=question,
        )
    )
    # return redirect(url_for('about'))


@app.route("/feedback", methods=["POST"])
@login_required
def feedback():
    feedback_text = request.form.get("feedback")
    problem_text = request.form.get("problem_text")
    if problem_text == "":
        problem_text = request.form.get("p")
    print(f"feedback : {feedback_text}")
    print(f"problem_text:{problem_text}")
    print(os.getcwd())
    # Load the pickled model file
    with open(
        r"C:\Users\oussa\Desktop\Educational_interactive_platform\app\static\models\sentimentAnalysis_model.sav",
        "rb",
    ) as f:
        model = pickle.load(f)
    # Load the pickled vectorizer file
    with open(
        r"C:\Users\oussa\Desktop\Educational_interactive_platform\app\static\models\sentimentAnalysis_vectorizer.sav",
        "rb",
    ) as f:
        vectorizer = pickle.load(f)
    # Vectorize the user's feedback
    feedback_vector = vectorizer.transform([feedback_text])
    # Predict the sentiment of the user's feedback
    sentiment = model.predict(feedback_vector)[0]
    print(f"sentiment : {sentiment}")
    print(f"sentiment type {type(sentiment)}")
    # Get the question object from the database
    question = Question.query.filter_by(question_text=problem_text).first()
    # Create a new feedback object
    feedback = Feedback(
        question_id=question.id,
        user_id=current_user.id,
        feedback_text=feedback_text,
        type=str(sentiment),
    )
    db.session.add(feedback)
    db.session.commit()
    flash("Feedback submitted successfully!", "success")
    return redirect(url_for("home"))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))
