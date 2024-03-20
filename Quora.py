from tkinter import filedialog
from tkinter import *

import selenium.common.exceptions
import self as self
from selenium.webdriver.common.action_chains import ActionChains
import tkinter as tk
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from pynput.keyboard import Key, Controller
import random
import urllib
import os
import keyboard
from keyboard import press
import sys
import time
import pyautogui
from datetime import datetime
from datetime import timedelta
import requests

chrome_options = webdriver.ChromeOptions()

# varaible
global List
List = []
global answList
global accList
global accountList
accountList = []

proxyList = []
accList = []
answList = []
#

global path_file
global uservalue
global passvalue
global timevalue
global userLink
flag = 0
keyboard = Controller()

audioToTextDelay = 10
delayTime = 2
audioFile = "\\payload.mp3"
SpeechToTextURL = "https://speech-to-text-demo.ng.bluemix.net/"


def delay():
    time.sleep(random.randint(2, 3))


def audioToText(audioFile):
    driver.execute_script('''window.open("","_blank")''')
    driver.switch_to.window(driver.window_handles[1])
    driver.get(SpeechToTextURL)

    delay()
    audioInput = driver.find_element(By.XPATH, '//*[@id="root"]/div/input')
    audioInput.send_keys(audioFile)

    time.sleep(audioToTextDelay)

    text = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[7]/div/div/div/span')
    while text is None:
        text = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[7]/div/div/div/span')

    result = text.text

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    return result


def quoraRecaptcha():
    time.sleep(5)
    iframes = driver.find_elements_by_tag_name('iframe')
    # print(iframes)
    # print(len(iframes))
    if len(iframes) == 1 or len(iframes) < 4:
        pass
    else:

        driver.switch_to.frame(iframes[0]);

        driver.find_element_by_class_name("recaptcha-checkbox-border").click()
        driver.switch_to.default_content()
        iframes = driver.find_elements_by_tag_name('iframe')
        audioBtnFound = False
        audioBtnIndex = -1

        for index in range(len(iframes)):
            driver.switch_to.default_content()
            iframe = driver.find_elements_by_tag_name('iframe')[index]
            driver.switch_to.frame(iframe)
            driver.implicitly_wait(delayTime)
            try:
                audioBtn = driver.find_element_by_id("recaptcha-audio-button")
                audioBtn.click()
                audioBtnFound = True
                audioBtnIndex = index
                break
            except Exception as e:
                pass

        if audioBtnFound:
            try:
                while True:
                    # get the mp3 audio file
                    src = driver.find_element_by_id("audio-source").get_attribute("src")
                    print("[INFO] Audio src: %s" % src)

                    # download the mp3 audio file from the source
                    urllib.request.urlretrieve(src, os.getcwd() + audioFile)

                    # Speech To Text Conversion
                    key = audioToText(os.getcwd() + audioFile)
                    print("[INFO] Recaptcha Key: %s" % key)

                    driver.switch_to.default_content()
                    iframe = driver.find_elements_by_tag_name('iframe')[audioBtnIndex]
                    driver.switch_to.frame(iframe)

                    # key in results and submit
                    inputField = driver.find_element_by_id("audio-response")
                    inputField.send_keys(key)
                    delay()
                    inputField.send_keys(Keys.ENTER)
                    delay()

                    err = driver.find_elements_by_class_name('rc-audiochallenge-error-message')[0]
                    if err.text == "" or err.value_of_css_property('display') == 'none':
                        print("[INFO] Success!")
                        break

            except Exception as e:
                print(e)
                sys.exit("[INFO] Possibly blocked by google. Change IP,Use Proxy method for requests")
        else:
            print("[INFO] Audio Play Button not found! In Very rare cases!")


# to run bot
def run_ALl():
    open_Browser()


def upvote():
    # try:
    #
    #     val = 20
    #     for i in range(5):
    #         indexpage = str(val)
    #         xpathFollow = "(//div)['" + indexpage + "']"
    #         # xpathFollow = "//span[@aria-label='Upvote']//span//*[name()='svg']//*[name()='path' and contains(@class,'icon_svg-s')]"
    #         xpathFollow.click()
    #         val = val + 4
    # except Exception:
    #     pass

    linkTime = LinkTimevalue.get()
    print(linkTime)
    # global driver
    for j in answList:
        print(j)
        driver.get(j)
        try:
            time.sleep(3)
            downvoteXpath = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[@aria-label='Upvote']//span//*[name()='svg']")))
            downvoteXpath.click()
        except Exception:
            try:
                time.sleep(3)
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//span[@aria-label='Upvote']//span//*[name()='svg']//*[name()='path' and contains(@class,'icon_svg-s')]")))
            except Exception:
                pass

        time.sleep(linkTime)


# open browser

def open_Browser():
    accTime = AccTimeValue.get()
    # print(accTime)
    global driver
    # print(len(accList))
    # print(len(proxyList))
    # print(proxyList)
    f = open("OutDataEmails.txt", "w+")
    global pIndex
    pIndex = 0
    row = 0
    column = 0

    while pIndex in range(len(proxyList)):
        print(pIndex)
        chrome_options.add_argument('--proxy-server=%s' % proxyList[pIndex])
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")

        driver = webdriver.Chrome(executable_path="chromedriver.exe", options=chrome_options)
        # driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
        driver.maximize_window()
        driver.get('https://www.quora.com/')
        # loging into qoura

        print("loging into account\n")
        QuoraUserName = accList[row][column]
        print(QuoraUserName)
        userXpath = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@id='email']")))
        userXpath.send_keys(QuoraUserName)
        userXpath.send_keys(Keys.ENTER)
        column = column + 1
        QuoraPassword = accList[row][column]
        pasXpath = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='password']")))
        pasXpath.send_keys(QuoraPassword)
        pasXpath.send_keys(Keys.ENTER)
        time.sleep(10)
        quoraRecaptcha()
        driver.switch_to.default_content()
        time.sleep(2)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(@type,'button')]"))).click()
            time.sleep(3)
        except Exception:
            pass
        try:
            time.sleep(3)
            CodeXpath = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='6 digit code']")))
            skiprow = CodeXpath.is_displayed()
            print(skiprow, "verfication will doing.....", QuoraUserName)

            driver.execute_script('''window.open("","_blank")''')
            driver.switch_to.window(driver.window_handles[1])
            driver.get("https://e.mail.ru/login?from=portal")
            try:
                keyboard = Controller()
                keyboard.type(QuoraUserName)
                keyboard.press(Key.enter)
                keyboard.release(Key.enter)

                # WebDriverWait(driver, 10).until(
                #     EC.presence_of_element_located((By.XPATH, "//input[@name='username']"))).send_keys(
                #     QuoraUserName)
                # WebDriverWait(driver, 10).until(
                #     EC.presence_of_element_located((By.XPATH, "//input[@name='username']"))).send_keys(Keys.ENTER)
                time.sleep(5)
                keyboard.type(QuoraPassword)
                print(QuoraPassword)
                keyboard.press(Key.enter)
                keyboard.release(Key.enter)
                driver.get("https://e.mail.ru/inbox")
                driver.switch_to.window(driver.window_handles[0])
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'Resend code')]"))).click()
                driver.switch_to.window(driver.window_handles[1])
                driver.get("https://e.mail.ru/inbox")
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                    (By.XPATH, "//span[@title='Quora Account Safety Team <noreply@quora.com>']"))).click()
                codeVeri = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                                           "//*[@id='simple-content-row_mr_css_attr']/td/table/tbody/tr/td[1]/table/tbody/tr/td/p[5]"))).text
                print(codeVeri)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                CodeXpath.send_keys(codeVeri)
                time.sleep(2)
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'Submit')]"))).click()
            except Exception:
                print("do manull login")
                pause = input()


            if row == (len(accList) - 1):
                break

            if pIndex == (len(proxyList) - 1):
                pIndex = 0
                print("\n[info]: Ip rotating IP")
                column = 0
                row = row + 1
                driver.close()
                continue

        except selenium.common.exceptions.TimeoutException:
            pass
        upvote()
        time.sleep(accTime)
        if row == (len(accList) - 1):
            break
        else:
            pass
        if pIndex == (len(proxyList) - 1):
            pIndex = 0
            print("\n[info]: Ip rotating IP")
            column = 0
            row = row + 1
            driver.close()
            continue
        else:
            pass
        driver.close()
        column = 0
        row = row + 1
        pIndex += 1
    f.close()


def splitAcc(accList):
    for i in accList:
        if ':' in i:
            accountList.append(i.split(':'))


def displayText(path):
    file = open(path, "r")
    Counter = 0

    # Reading from file
    Content = file.read()
    CoList = Content.split("\n")
    for i in CoList:
        if i:
            List.append(i)
            Counter += 1
    return Counter


# browse button
def answer_button():
    global answList
    directory1 = filedialog.askopenfilename(filetypes=(("links insert", "*.txt"), ("All files", "*")))
    # directory.repalce('/','\')
    a_path.set(directory1)
    ansNumValue.set(displayText(directory1))
    answList = List.copy()
    List.clear()

    print(answList)


def proxy_button():
    global proxyList
    directory2 = filedialog.askopenfilename(filetypes=(("proxy text files", "*.txt"), ("All files", "*")))
    # directory.repalce('/','\')
    p_path.set(directory2)
    proxyNumValue.set(displayText(directory2))
    proxyList = List.copy()
    List.clear()


def acc_button():
    global accList
    directory3 = filedialog.askopenfilename(filetypes=(("account text files", "*.txt"), ("All files", "*")))
    # directory.repalce('/','\')
    ac_path.set(directory3)
    accNumValue.set(displayText(directory3))
    accList = List.copy()
    List.clear()
    splitAcc(accList)
    accList = accountList.copy()
    accountList.clear()
    print(accList)


root = Tk()
root.geometry("1000x600")
root.title("Bot By DEEPAK www.thengdeveloper.com")

root['background'] = '#9ab2f0'
# bg = PhotoImage(file="bg.png")
# bg_lable = Label(root, image=bg)
# bg_lable.place(x=0, y=0, relwidth=1, relheight=1)

# credential

answerLable = Label(root, text="Answers List :", font="Roboto,14,bold", bg="#9ab2f0", fg="black")
aNumLable = Label(root, text="Answers :", font="Roboto,14,bold", bg="#a6ace7", fg="black")
AccLable = Label(root, text="Account List :", font="Roboto,14,bold", bg="#99b2f2", fg="black")
AcNumLable = Label(root, text="Account :", font="Roboto,14,bold", bg="#acc1ec", fg="black")
ProxyLable = Label(root, text="Proxy List :", font="Roboto,14,bold", bg="#9dafed", fg="black")
PrNumLable = Label(root, text="Proxy :", font="Roboto,14,bold", bg="#aac6ee", fg="black")
intervalLableLink = Label(root, text="Intervel between Reporting links in seconds :", font="Roboto,14,bold",
                          bg="#aab0ed", fg="black")
intervalAccLble = Label(root, text="Intervel between Switching accs in seconds:", font="Roboto,14,bold", bg="#aab0ed",
                        fg="black")

# path of files
a_path = StringVar()
ac_path = StringVar()
p_path = StringVar()
ansPathLable = Label(master=root, textvariable=a_path)
accPathLable = Label(master=root, textvariable=ac_path)
proxyPathLable = Label(master=root, textvariable=p_path)

# path alignment

ansPathLable.grid(row=0, column=1)
accPathLable.grid(row=1, column=1)
proxyPathLable.grid(row=2, column=1)
# num value lable

aNumLable.grid(row=14, column=0)
AcNumLable.grid(row=14, column=2)
PrNumLable.grid(row=14, column=4)

# alignment of layout
answerLable.grid(row=0)
AccLable.grid(row=1)
ProxyLable.grid(row=2)
intervalAccLble.grid(row=3)
intervalLableLink.grid(row=4)
ansNumValue = IntVar()
answerNumLable = Label(master=root, textvariable=ansNumValue)
answerNumLable.grid(row=14, column=1)
accNumValue = IntVar()
AccNumLable = Label(master=root, textvariable=accNumValue)
AccNumLable.grid(row=14, column=3)
proxyNumValue = IntVar()
ProxyNumLable = Label(master=root, textvariable=proxyNumValue)
ProxyNumLable.grid(row=14, column=5)
# entry
LinkTimevalue = IntVar()
AccTimeValue = IntVar()
timeentry1 = Entry(root, textvariable=AccTimeValue)
timeentry2 = Entry(root, textvariable=LinkTimevalue)
timeentry1.grid(row=3, column=2)
timeentry2.grid(row=4, column=2)
# data


buttonAnswer = Button(text="Browse", command=answer_button).grid(row=0, column=2)

buttonAcc = Button(text="Browse", command=acc_button).grid(row=1, column=2)

buttonProxy = Button(text="Browse", command=proxy_button).grid(row=2, column=2)

Button(text="Run Bot", command=run_ALl).grid()
root.mainloop()
