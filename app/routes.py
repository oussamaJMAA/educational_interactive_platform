from flask import  render_template, request, redirect, url_for, flash , session
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
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from app.models import User , Question, Feedback
from app import app , db , bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import os 
import openai
import base64
import requests
import gradio as gr
openai.api_key = "api_key"
import random
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def download_image(problem_text):
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    '''
    chrome_options.add_experimental_option("prefs", {
    "download.default_directory": "C:/Users/oussa/Desktop/Educational_interactive_platform/app/static/uploads",
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})
'''
    chrome_driver_path = "C:/DsProjects/chromedriver.exe"
    #gr.load("models/oussama120/wp-converter").launch(share=True)

    #browser = webdriver.Chrome(executable_path=chrome_driver_path,options=chrome_options)
    browser = webdriver.Chrome(executable_path=chrome_driver_path)
    browser.get("http://127.0.0.1:7860")
    wait_textarea = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "textarea"))
    )
    textarea = browser.find_element(By.TAG_NAME,'textarea')
    textarea.send_keys(problem_text)
    submit_button = browser.find_element(By.XPATH, '//button[text()="Submit"]')
    submit_button.click()
    #wait up to 10 seconds for the element to be clickable
    div_element = WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[aria-label="Download"]')))
    # click the element
    div_element.click()
    time.sleep(5)
    #renaming image
    ############################################
    os.chdir('C:/Users/oussa/Downloads/')
  # Get a list of all files in the directory
    files = os.listdir()

    # Filter for image files (e.g., .jpg, .png, etc.)
    image_files = [file for file in files if file.endswith('.jpg') or file.endswith('.png')]

    # Sort the image files by creation time (newest to oldest)
    image_files.sort(key=os.path.getctime, reverse=True)
    #get 3 random number and characters concatenated
    random_number = random.randint(100, 99999)
    random_char = random.sample('abcdefghijklmnopqrstuvwxyz', 4)
    print(random_char) 
    #concatenate the random number and character
    random_number_char = str(random_number) + ''.join(random_char)
    # Rename the last image file to a new name
    new_name = f'image {random_number_char}.jpg' # Replace with your desired new name
    os.rename(image_files[0], new_name)
    ############################################
     # Source file path
    src_path = f"C:/Users/oussa/Downloads/{new_name}"
    
    # Destination file path
    dst_path = r"C:\Users\oussa\Desktop\Educational_interactive_platform\app\static\uploads"

    # Copy the file from source to destination
    shutil.copy(src_path, dst_path)
   
    return  f"image {random_number_char}.jpg"

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

def generate_image2(problem_text):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    browser = webdriver.Chrome(options=chrome_options)
    #browser = webdriver.Chrome()
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
    #img_element.screenshot(r'C:\Users\oussa\Desktop\Educational_interactive_platform\app\static\uploads\image1.png')
    #image_url = 'C:/Users/oussa/Desktop/Educational_interactive_platform/app/static/uploads/image1.png'
    #img_url = os.path.join('uploads', 'image1.png')
    img_data = img_element.screenshot_as_base64

    # Save the image to a file in the 'static/uploads' folder of the Flask app
    filename = 'image1.png'
    filepath = os.path.join('app', 'static', 'uploads', filename)
    with open(filepath, 'wb') as f:
        f.write(base64.b64decode(img_data))

    # Return the URL to the image file, relative to the Flask app's static folder
    img_url = 'uploads/' + filename
    return img_url
    



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
        question = Question(question_text=problem_text, user_id=current_user.id)
        db.session.add(question)
        db.session.commit()
        #img_url=generate_image2(problem_text)
        # Generate the math problem image and return it to the user
        #img_url = generate_image2(problem_text)
        img_url = download_image(problem_text)
        print("img_url",img_url)
        print("problem",problem_text)
        '''
        data = {"inputs": problem_text}
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        img_url = loop.run_until_complete(get_image_url(data))
        '''
        # Render the template with img_url
        return render_template("about.html", img_url=img_url, problem_text=problem_text)
    #is_correct = session.get('is_correct')
    #answer_text = session.get('answer_text')
    #img_url = session.get('img_url1')
    #correct_answer = session.get('correct_answer')
    is_correct = request.args.get('is_correct')
    answer_text = request.args.get('answer_text')
    img_url = request.args.get('img_url1')
    correct_answer = request.args.get('correct_answer')
    p = request.args.get('problem_text')
    print(f"answer_text: {answer_text}")
    print(f"is_correct: {is_correct}")
    print(f"correct_answer: {correct_answer}")
    print(f"img_url: {img_url}")
    # Open thumbnail image with PIL
    
    
    if img_url:
        '''
        # Render the template with img_url and answer_text
        thumbnail_data = base64.b64decode(img_url.split(',')[1])
        thumbnail_img = Image.open(BytesIO(thumbnail_data))

# Resize thumbnail image
        thumbnail_img.thumbnail((600, 600))

# Convert image to bytes
        thumbnail_img_bytes = BytesIO()
        thumbnail_img.save(thumbnail_img_bytes, format='JPEG')
        thumbnail_img_bytes = thumbnail_img_bytes.getvalue()
        
# Encode image as base64 string
        resized_url = 'data:image/jpeg;base64,' + base64.b64encode(thumbnail_img_bytes).decode('utf-8')
        '''
        return render_template("about.html", img_url=img_url, problem_text=request.form.get("problem_text"), answer_text=answer_text, is_correct=is_correct,correct_answer=correct_answer,p=p)

    # Render the template without img_url or answer section
    return render_template("about.html", problem_text="", is_correct=is_correct, answer_text="", img_url="") 







    

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
        return (True,rep)
    else:
        return (False,rep)

@app.route('/answer', methods=['POST'])
def check_answer():
    user = current_user
    curr_level = user.level
    answer_text = request.form.get('answer')
    question = request.form.get('problem_text')
    is_correct = check_if_answer_is_correct(question,answer_text)[0]
    correct_answer = check_if_answer_is_correct(question,answer_text)[1]
    user.add_answer(answer_text, is_correct)
    user.nb_attempts += 1
    db.session.commit()
    if user.nb_attempts == 3:
        level = user.get_level(curr_level)
        user.level = level
        user.nb_attempts = 0
        db.session.commit()  
    img_url = request.form.get('img_url1')
    print(img_url)
    '''
    img_data = base64.b64decode(img_url.split(',')[1])
# Open image with PIL
    img = Image.open(BytesIO(img_data))
# Resize image to thumbnail size
    img.thumbnail((128, 128))
# Convert image to bytes
    img_bytes = BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes = img_bytes.getvalue()
# Encode image as base64 string
    thumbnail_url = 'data:image/jpeg;base64,' + base64.b64encode(img_bytes).decode('utf-8')
    # session['is_correct'] = is_correct
    # session['answer_text'] = answer_text
    # session['img_url1'] = thumbnail_url
    # session['correct_answer'] = correct_answer
    '''
    return redirect(url_for('about', is_correct=is_correct, answer_text=answer_text, img_url1=img_url,correct_answer=correct_answer,problem_text=question))
    #return redirect(url_for('about'))


  
@app.route('/feedback', methods=["POST"])
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
    with open(r'C:\Users\oussa\Desktop\Educational_interactive_platform\app\static\models\sentimentAnalysis_model.sav', 'rb') as f:
        model = pickle.load(f)
    # Load the pickled vectorizer file
    with open(r'C:\Users\oussa\Desktop\Educational_interactive_platform\app\static\models\sentimentAnalysis_vectorizer.sav', 'rb') as f:
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
    feedback = Feedback(question_id=question.id, user_id=current_user.id, feedback_text=feedback_text,type=str(sentiment))
    db.session.add(feedback)
    db.session.commit()
    flash('Feedback submitted successfully!', 'success')
    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))