import os
from flask import Flask, flash, request, redirect, url_for,render_template
from werkzeug.utils import secure_filename
from selenium.webdriver.common.keys import Keys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from time import sleep
from urllib.parse import quote

ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__)
app.secret_key="jayho"
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def sendmsg():

    options = Options()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--profile-directory=Default")
    options.add_argument("--user-data-dir=/var/tmp/chrome_user_data")

    os.system("")
    os.environ["WDM_LOG_LEVEL"] = "0"
    m = open("message.txt", "r")
    message = m.read()
    m.close()

    print('\nThis is your message-')
    print( message)
    print("\n")
    message = quote(message)

    numbers = []
    f = open("numbers.txt", "r")
    for line in f.read().splitlines():
        if line.strip() != "":
            numbers.append(line.strip())
    f.close()
    total_number=len(numbers)
    print('We found ' + str(total_number) + ' numbers in the file' )
    delay = 30

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    print('Once your browser opens up sign in to web whatsapp')
    driver.get('https://web.whatsapp.com')
    #input("AFTER logging into Whatsapp Web is complete and your chats are visible, press ENTER...")
    for idx, number in enumerate(numbers):
        number = number.strip()
        if number == "":
            continue
        print( '{}/{} => Sending message to {}.'.format((idx+1), total_number, number))
        try:
            url = 'https://web.whatsapp.com/send?phone=+91' + number + '&text=' + message
            sent = False
            for i in range(3):
                if not sent:
                    driver.get(url)
                    try:
                        click_btn = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='_4sWnG']")))
                    except Exception as e:
                        print(f"\nFailed to send message to: {number}, retry ({i+1}/3)")
                        print("Make sure your phone and computer is connected to the internet.")
                        print("If there is an alert, please dismiss it." )
                    else:
                        #driver.find_element_by_xpath("//*[@id='main']/footer/div[2]/div/span[2]/div/div[2]/div[1]/div/div[2]").send_keys(Keys.RETURN)
                        sleep(1)
                        click_btn.click()
                        sent=True
                        sleep(3)
                        print('Message sent to: ' + number )
        except Exception as e:
            print('Failed to send message to ' + number + str(e) )
    driver.close()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':  
        f = request.files['msg']  
        f.save(f.filename)  
        f1= request.files['numbers']
        f1.save(f1.filename.format("numbers.txt"))
        sendmsg()

    return  render_template('index.html')
if __name__ == "__main__":
    app.run(debug=True)