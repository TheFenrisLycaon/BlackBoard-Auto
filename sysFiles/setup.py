import subprocess
import os
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from time import sleep
    from datetime import datetime as date
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.action_chains import ActionChains
    print("Successful")
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

    def setCourses(self):
        driver = self.driver
        sleep (10)
        page = driver.find_element_by_css_selector('#main-content-inner > div')
        k = '#main-heading'            
        body = driver.find_element_by_css_selector(k)
        body.click()
        body.send_keys(Keys.PAGE_DOWN)
        sleep(2)
        body.send_keys(Keys.PAGE_DOWN)
        sleep(2)

        codes = []
        names = []
        subcodes = []
        
        for item in page.find_elements_by_xpath('//*[@class="default-group term-"]'):
            courseid = item.find_element_by_css_selector('bb-base-course-card > div').get_attribute('data-course-id')
            codes.append(courseid)
            names.append(item.find_element_by_css_selector('#course-link-{} > h4'.format(courseid)).get_attribute('title'))
            subcodes.append(item.find_element_by_css_selector('#course-list-course-{} > div.element-details.summary > div.multi-column-course-id'.format(courseid)).text)

        for item in page.find_elements_by_xpath('//*[@class="default-group term- last-item"]'):
            courseid = item.find_element_by_css_selector('bb-base-course-card > div').get_attribute('data-course-id')
            codes.append(courseid)
            names.append(item.find_element_by_css_selector('#course-link-{} > h4'.format(courseid)).get_attribute('title'))
            subcodes.append(item.find_element_by_css_selector('#course-list-course-{} > div.element-details.summary > div.multi-column-course-id'.format(courseid)).text)

        # print(codes)
        # print(names)
        # print(subcodes)
        links = []
        for i in codes:
            links.append('https://cuchd.blackboard.com/ultra/courses/'+i+'/outline')
        # print(links)

        for i in range(len(codes)):
            self.courses.append((i+1,names[i], links[i],subcodes[i][:7]))

        courseFile = './Data/.courseFile'
        
        with open(courseFile, 'w') as fileIn:
            for i in range(len(codes)):
                fileIn.write("{} :: {} :: {} :: {}\n".format(i+1,names[i], links[i],subcodes[i][:7]))


    def setCalender(self):
        self.weekdays = [('MON', []), ('TUE', []), ('WED', []), ('THU', []), ('FRI', []), ('SAT', [])]
        
        for i in range(len(self.courses)):
            print(self.courses[i][0], '\t', self.courses[i][3], '\t', self.courses[i][1])
        
        print('Now set-up your daily calender.\tEnter the sub-codes as given above, enter 0 if you have no class or mid-day break.\nFor example if you have classes 1, 2, 3, break, 4 and 5 on the first day,\tEnter 1 2 3 0 4 5\n:')
        
        for k in range(6):
            restart = True
            while restart == True:
                restart = False
                userInpCal = list(map(int, input('{}::'.format(self.weekdays[k][0])).split()))
        
                for _ in range(len(userInpCal)):
                    if userInpCal[_] == 0:
                        userInpCal[_] = None
                    if userInpCal[_] != None and userInpCal[_] > len(self.courses):
                        print("Error, you only have {} subjects!\nTry again!".format(len(self.courses)))
                        restart = True
                        break

                for item in userInpCal:
                    if item != None:
                        couLink = self.courses[item-1][2]
                    else:
                        couLink = None
                    self.weekdays[k][1].append(couLink)


        calFile = './Data/.calFile'

        with open(calFile, 'w') as fileIn:
            for i in range(6):
                fileIn.write('{} : {}\n'.format(self.weekdays[i][0], self.weekdays[i][1]))


    def __init__(self):
        self.username = str(input('Enter Username ::\t'))
        self.password = str(input('Enter Password ::\t'))
        cred = '.doNotTouch'
            
        if os.path.isdir('Data'):
            pass
        else:
            os.makedirs('Data')
        cred = './Data/.doNotTouch'

        with open(cred, 'w') as fileIn:
            fileIn.write("{}\n{}".format(self.username,self.password))

        self.courses = []
        self.weekdays = [None, None, None, None, None, None]
        self.driver = webdriver.Chrome(
            executable_path=r"./sysFiles/chromedriver", options=set_opt())
        self.driver.get("https://cuchd.blackboard.com/?new_loc=%2Fultra%2Fcourse")
        sleep(2)
        
        
    def gettingStarted(self):
        print('Getting your courses... PLease Wait')
        self.setCourses()
        print('{} courses found'.format(len(self.courses)))
        self.setCalender()

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

    def bye(self):
        driver = self.driver
        driver.quit()


        

if __name__ == "__main__":
    set_opt()
    x = BB()
    x.login()
    day = date.today().strftime("%A")
    rn = int(date.now().strftime("%H%M"))
    print("You logged in on " + str(day) + " at " + str(rn) + " hours !" )
    x.gettingStarted()

    comp = './Data/.setupComp'

    with open(comp, 'w') as fileIn:
        fileIn.write('Welcome to future !!!')

    input()

    x.bye()