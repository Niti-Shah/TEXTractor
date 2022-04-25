# Important imports
from app import app
from flask import request, render_template
import cv2
import numpy as np
from PIL import Image
import os
import random
import string
import pytesseract
import pyttsx3
from gtts import gTTS

# Adding path to config
app.config['INITIAL_FILE_UPLOADS'] = 'app/static/uploads' #check the size of img and ration bw text and image

new_string1 = ""
# @app.route('/')
# def index():
#     register_form = RegisterForm()
#     login_form = LoginForm()
#     return render_template('index.html', register_form=register_form, login_form=login_form)


@app.route('/', methods=['GET', 'POST'])
def textractor():
    return render_template('textractor.html')


# Route to home page
@app.route("/index", methods=["GET", "POST"])
def index():

	# Execute if request is get
	if request.method == "GET":
		full_filename =  'images/white_bg.jpg' #taking dummy image from image folder 
		return render_template("index.html", full_filename = full_filename) #bascically displaying initial dummy image on flask interface and code assigns LHS "full_filename" it to the same name in the index.html file and pastes it there

	# Execute if reuqest is post
	if request.method == "POST":
		image_upload = request.files['image_upload'] #gets the uploaded image from the index.html file named "image_upload"
		imagename = image_upload.filename
		image = Image.open(image_upload) #used to open image using the PIL (pyhton imaging library)

		# Converting image to array
		image_arr = np.array(image.convert('RGB')) #converting RGB image to array of prooerties of image
		# Converting image to grayscale
		gray_img_arr = cv2.cvtColor(image_arr, cv2.COLOR_BGR2GRAY)#converting to greyscale cuz dimensiondecreases
		#Converting image back to rbg
		image = Image.fromarray(gray_img_arr)

		# Printing lowercase
		letters = string.ascii_lowercase #generates all lowercase alphabets
		# Generating unique image name for dynamic image display
		name = ''.join(random.choice(letters) for i in range(10)) + '.png'
		full_filename =  'uploads/' + name

		# Extracting text from image
		custom_config = r'-l eng --oem 3 --psm 6' #language is selected as eng, oem specifies OCR engine mode, 3 is default, PSM is page segmentation mode, 6 is single uniform block of text.
		text = pytesseract.image_to_string(image,config=custom_config)

		# Remove symbol if any
		# characters_to_remove = "!()@—*“>+-/,'|£#%$&^_~" 
		new_string = text
		new_string1 = text
		# for character in characters_to_remove: 
		# 	new_string = new_string.replace(character, "")

		#text to speech part--------------------------------------------------------------------
		f = open("output.txt", "w")
		f.write(new_string1)


		# Converting string into list to dislay extracted text in seperate line
		new_string = new_string.split("\n") #detects new line in image and displays text accordingly on a new line

		# Saving image to display in html
		img = Image.fromarray(image_arr, 'RGB') 
		img.save(os.path.join(app.config['INITIAL_FILE_UPLOADS'], name))

		# Returning template, filename, extracted text
		return render_template('index.html', full_filename = full_filename, text = new_string)


def text_to_speech(text, gender):
    voice_dict = {'Male': 0, 'Female': 1}
    code = voice_dict[gender]

    engine = pyttsx3.init()

    # Setting up voice rate
    engine.setProperty('rate', 125)

    # Setting up volume level  between 0 and 1
    engine.setProperty('volume', 0.8)

    # Change voices: 0 for male and 1 for female
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[code].id)

    engine.say(text)
    engine.runAndWait()

@app.route('/voice', methods=['POST', 'GET'])
def voice():
    if request.method == 'POST':
		# read_string = open("output.txt", "r")
        text = "hello"
        gender = request.form['voices']
        text_to_speech(text, "Male")
        return render_template('voice.html')
    else:
        return render_template('voice.html')



# Main function
if __name__ == '__main__':
    app.run(debug=True)
