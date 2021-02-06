import subprocess
import ast
import sys
import os
from threading import Timer

timestamps = [945, 1045, 1145, 1245, 1330, 1430, 1530]

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from time import sleep
    from datetime import datetime as date
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.action_chains import ActionChains
    # print("Successful")
except:
    print('Installing imports')
    install('selenium')

def set_opt():        
    opt = Options()
    opt.add_argument("--disable-infobars")
    opt.add_argument("start-maximized")
    opt.add_argument("--disable-extensions")
    opt.add_argument('--ignore-certificate-errors-spki-list')
    opt.add_argument('--ignore-ssl-errors')
    opt.add_experimental_option("excludeSwitches", ["enable-logging", 'enable-automation'])
    opt.add_experimental_option("prefs", { \
        "profile.default_content_setting_values.media_stream_mic": 1, 
        "profile.default_content_setting_values.media_stream_camera": 1,
        "profile.default_content_setting_values.geolocation": 1, 
        
        "profile.default_content_setting_values.notifications": 1,
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    })
    return opt


class BB:

    def __init__(self):
        cred = './Data/.doNotTouch'
        
        try:
            with open(cred, 'r') as fileIn:
                self.username, self.password = fileIn.read().split()
                
                # print(self.username)
                # print(self.password)
        except:
            print("No File, run your installation file again!!!")
        
        courseFile = './Data/.courseFile'
        calFile = './Data/.calFile'
            
        with open(calFile, 'r') as fileIn:
            self.weekdays = fileIn.read().split('\n') 

        self.days = []
        for i in range(6):
            self.days.append(ast.literal_eval(self.weekdays[i][6:]))
        
        # for _ in self.days:
        #     print(_)

        self.driver = webdriver.Chrome(
            executable_path=r"./sysFiles/chromedriver", options=set_opt())
        self.driver.get("https://cuchd.blackboard.com/?new_loc=%2Fultra%2Fcourse")
        sleep(2)

   
    def login(self):
        driver = self.driver
        try:
            driver.find_element_by_xpath('//*[@id="agree_button"]')\
                .click()
            driver.find_element_by_xpath('//*[@id="user_id"]')\
                .send_keys(self.username)
            driver.find_element_by_xpath('//*[@id="password"]')\
                .send_keys(self.password)
            driver.find_element_by_xpath('//*[@id="entry-login"]')\
                .click()
            sleep(4)
        except:
            print("Wrong username or password !!! Try Again !!!")
            self.login()

    def begin(self,x,y):
        if x == 'Monday':
            self.bring(self.days[0],y)
        elif x == 'Tuesday':
            self.bring(self.days[1],y)
        elif x == 'Wednesday':
            self.bring(self.days[2],y)
        elif x == 'Thursday':
            self.bring(self.days[3],y)
        elif x == 'Friday':
            self.bring(self.days[4],y)
        elif x == 'Saturday':
            self.bring(self.days[5],y)
        else:
            print("It's a holiday, pal! Enjoy !")
            pass

    def bring(self,x,y):
        day = x
        # print(x[0])
        driver = self.driver

        if y < 945:
            print("Hold ON !!!")
            sleep(((945 - y)//100)*3600 + ((945-y)%100)*60)
            y = int(date.now().strftime("%H%M"))
            self.bring(x,y)
        elif y >= 945 and y < 1045:
            t = 0
        elif y >= 1045 and y < 1145:
            t = 1
        elif y >= 1145 and y < 1245:
            t = 2
        elif y >= 1245 and y < 1330:
            t = 3
        elif y >= 1330 and y < 1430:
            t = 4
        elif y >= 1430 and y < 1530:
            t = 5
        else:
            print("You're too late to handle the power of spinjitzu !!!")
        
        classno = 0
        
        while y < 1530:
            timeWaiting = (((timestamps[t+1]//100)*60 + timestamps[t+1]%100)*60 - ((y//100)*60 + y%100)*60)
            
            if x[t] == None:
                print('No class right now... Waiting for ::\t' + str(timeWaiting) + ' seconds !')
                sleep(timeWaiting)
                t+=1
                y = int(date.now().strftime("%H%M"))
                continue
        
            else:
                driver.get(x[t])
                print("\nClass from " + str(timestamps[t]) + ' to ' + str(timestamps[t+1]))
            
            sleep(10)

            print("Getting Books !!!")
            driver.find_element_by_css_selector('#sessions-list-dropdown').click()
            sleep(1)
            print("Getting in Class !!!")
            try:
                driver.find_element_by_xpath('/html/body/div[1]/div[2]/bb-base-layout/div/main/div[3]/div/div[3]/div/div/div/div[2]/div/div[2]/div[3]/div/div[2]/div[3]/aside/div[6]/div[2]/div[2]/div/div/ul/li[2]/a').click()
                sleep(45)
            except:
                print('No class, BB error maybe !!!')
            
            driver.switch_to.window(driver.window_handles[-1])

            if classno == 0:
                print("Turning Mic On !")
                driver.find_element_by_css_selector("#dialog-description-audio > div.techcheck-controls.equal-buttons.buttons-2-md > button").click()
                sleep(10)
                print("Turning Video On !")
                driver.find_element_by_css_selector('#techcheck-video-ok-button').click()
                sleep(10)
                driver.find_element_by_css_selector('#announcement-modal-page-wrap > div > div.announcement-later-tutorial.ng-scope > button').click()
                sleep(1)
                try:
                    driver.find_element_by_css_selector('#tutorial-dialog-tutorials-menu-learn-about-tutorials-menu-close').click()
                    sleep(2)
                    driver.find_element_by_xpath('/html/body/div[1]/div[1]/main/bb-panel-open-control/div/button[1]').click()
                    sleep(1)
                    driver.find_element_by_xpath('/html/body/div[1]/div[1]/main/div[3]/section/div/div/ul/li/ul/li/bb-channel-list-item/button').click()
                    driver.find_element_by_xpath('//*[@id="channel-item-d74321ca-1af3-4008-a21a-6f38559f1924"]/span').click()
                    sleep(1)
                    timeWaiting -= 65
                except:
                    timeWaiting -= 60
            else:
                timeWaiting -= 20
            
            print("In class... Waiting for ::\t" + str(timeWaiting) + ' seconds !')
            
            wish = None
            timeout = 10
            timer = Timer(timeout, print, ['Sorry, times up'])
            timer.start()
            wish = str(input("Wish the prof?(y/n)\t"))
            timer.cancel()
            timeWaiting -= 10
            if 'y' in wish.lower():
                try:
                    print("Tryna Wish the professor !")
                    driver.find_element_by_xpath('//*[@id="message-input"]').click()
                    
                    if int(date.now().strftime("%H%M")) >= 1200 :
                        driver.find_element_by_xpath('//*[@id="message-input"]').send_keys("Good Afternoon everyone !!").send_keys(Keys.ENTER)
                    else:
                        driver.find_element_by_xpath('//*[@id="message-input"]').send_keys("Good Morning everyone !!").send_keys(Keys.ENTER)
                
                except:
                    print("Nah, not worth it !")
                    pass
            else:
                print('Okay')
            
            t += 1

            classno += 1
            sleep(timeWaiting)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            y = int(date.now().strftime("%H%M"))
        
        driver.quit()


if __name__ == "__main__":
    set_opt()
    x = BB()
    x.login()
    day = date.today().strftime("%A")
    rn = int(date.now().strftime("%H%M"))
    print("You logged in on " + str(day) + " at " + str(rn) + " hours !" )
    x.begin(day,rn)
    k = input("Press any key to exit...")