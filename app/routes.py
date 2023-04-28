from flask import  render_template, request, redirect, url_for, flash
from app.forms import RegistrationForm, LoginForm
import aiohttp
from io import BytesIO
from PIL import Image
import asyncio
import base64
import pytesseract
# import libraries for selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from app.models import User 
from app import app , db , bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import os 
import openai
openai.api_key = "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"

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def generate_image(problem_text):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    browser = webdriver.Chrome(options=chrome_options)

    # Navigate to the website
    browser.get("https://huggingface.co/oussama120/wp-converter")


    input_field = browser.find_element(By.XPATH,'//input[@placeholder="Your sentence here..."]')
    input_field.send_keys(problem_text)

    # Click on the compute button
    button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and text()='Compute']")))
    button.click()
    time.sleep(30)

def generate_image2(request,problem_text):
    #chrome_options = Options()
    #chrome_options.add_argument("--headless")
    #browser = webdriver.Chrome(options=chrome_options)
    browser = webdriver.Chrome()
    # Navigate to the website
    browser.get("https://huggingface.co/oussama120/wp-converter")
    input_field = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="Your sentence here..."]')))

    #input_field = browser.find_element(By.XPATH,'//input[@placeholder="Your sentence here..."]')
    input_field.send_keys(problem_text)
    #browser wait
    
    # Click on the compute button
    button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and text()='Compute']")))
    button.click()
    #wait time

    # Find the image element on the webpage
    img_element = WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.XPATH, '//img[@class="max-w-sm object-contain"]')))

   
    # Scroll down the webpage to capture the full image
    browser.execute_script("window.scrollBy(0, document.body.scrollHeight)")

    # Wait for the page to finish scrolling
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Get the base64-encoded image data from the 'src' attribute of the image element
    img_element.screenshot('static/image4.png')
    image_url = request.host_url + 'static/image4.png'
    
    return image_url



async def get_image_url(data):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://api-inference.huggingface.co/models/oussama120/wp-converter",
            headers={"Authorization": "Bearer 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"},
            json=data
        ) as response:
            image_data = await response.read() # Get response body as bytes
            try:
                image = Image.open(BytesIO(image_data)) # Create PIL image from bytes
            except:
                # Return a placeholder image if the actual image cannot be identified
                return "https://via.placeholder.com/400x300.png?text=Image+Not+Found"
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
            img_url = "data:image/jpeg;base64," + img_str
            return img_url

"""
async def get_image_url(data):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://api-inference.huggingface.co/models/oussama120/wp-converter",
            headers={"Authorization": "Bearer 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"},
            json=data
        ) as response:
            image_data = await response.read() # Get response body as bytes
            image = Image.open(BytesIO(image_data)) # Create PIL image from bytes
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
            img_url = "data:image/jpeg;base64," + img_str
            return img_url
"""
@app.route('/')
def home():
    return render_template('home.html',title="Home_Page")



def extract_text(img_path):
    im = Image.open(img_path)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Users\oussa\AppData\Local\Tesseract-OCR\tesseract.exe'
    text = pytesseract.image_to_string(im, lang = 'eng')
    return text

"""
@app.route('/about',methods=["GET", "POST"])
def about():
  img_url = None
  if request.method == "POST":
        data = {"inputs": request.form["text"]}
        #time.sleep(30) # Wait 30 seconds
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        img_url = loop.run_until_complete(get_image_url(data))
  return render_template("about.html", img_url=img_url)
"""
@app.route('/about', methods=["GET", "POST"])
@login_required
def about():
    if request.method == "POST":
        if 'problem_image' in request.files:
            file = request.files['problem_image']
            if file:
                # Save the uploaded file to a temporary location
                filepath = 'C:/Users/oussa/Desktop/Educational_interactive_platform/problem_image.png'
                file.save(filepath)

                # Extract the text from the image using OCR
                pytesseract.pytesseract.tesseract_cmd = r'C:\Users\oussa\AppData\Local\Tesseract-OCR\tesseract.exe'
                problem_text = pytesseract.image_to_string(Image.open(filepath))
                #generate_image(problem_text)
                # If an image was uploaded, render the template with problem_text
                return render_template("about.html", problem_text=problem_text)

        # If no image was uploaded, use the text input field value instead
        
        problem_text = request.form.get("text")
        generate_image(problem_text)
        # Generate the math problem image and return it to the user
        #img_url = generate_image2(request,problem_text)
        
        data = {"inputs": problem_text}
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        img_url = loop.run_until_complete(get_image_url(data))
        
        # Render the template with img_url
        return render_template("about.html", img_url=img_url, problem_text=problem_text)

    # Add this default return statement
    return render_template("about.html")




   


    

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        # if form is valid, then flash a success message
        flash(f'Account created for {form.username.data}!', 'success')
        # redirect to the home page
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    # if form is valid, then flash a success message
    if form.validate_on_submit():
         user = User.query.filter_by(email=form.email.data).first()
         if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
         else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
                
                
            
    
        
    return render_template('login.html', title='Login', form=form)


def check_if_answer_is_correct(question,answer):
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
    if rep == answer:
        return True
    else:
        return False
@app.route('/answer', methods=['POST'])
def check_answer():
    user = current_user
    answer_text = request.form.get('answer')
    question = request.form.get('problem_text')
    is_correct = check_if_answer_is_correct(question,answer_text) 
    user.add_answer(answer_text, is_correct)
    user.nb_attempts += 1
    db.session.commit()
    level = user.get_level()
    if user.nb_attempts ==3:
        user.level=level
        db.session.commit()  
    return redirect(url_for('about'))
    

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))