import subprocess
import os
import sys
import ast


class initialize:
    def __init__(self):
        try:
            from selenium import webdriver
            from selenium.webdriver.common.keys import Keys
            from time import sleep
            from datetime import datetime as date
            from selenium.webdriver.chrome.options import Options
            # print("Successful")
        except:
            print('Installing imports')
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", 'selenium'])

    def set_opt(self):
        opt = Options()
        opt.add_argument("--disable-infobars")
        opt.add_argument("start-maximized")
        opt.add_argument("--disable-extensions")
        opt.add_argument('--ignore-certificate-errors-spki-list')
        opt.add_argument('--ignore-ssl-errors')
        opt.add_experimental_option(
            "excludeSwitches", ["enable-logging", 'enable-automation'])
        opt.add_experimental_option("prefs", {
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
        if os.path.isdir('Data'):
            pass
        else:
            os.makedirs('Data')

        if '.cred' not in os.listdir('./Data'):
            self.username = str(input('Enter Username ::\t'))
            self.password = str(getpass('Enter Password ::\t'))
        else:
            print("Credentials Found... Logging in...")
            with open('./Data/.cred', 'r') as fileIn:
                self.username, self.password = fileIn.read().split()

        self.courses = []
        self.weekdays = [None, None, None, None, None, None]
        self.driver = webdriver.Chrome(
            executable_path=r"./sysFiles/chromedriver", options=set_opt())
        self.driver.get(
            "https://cuchd.blackboard.com/?new_loc=%2Fultra%2Fcourse")
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

    def gettingStarted(self):
        print('Getting your courses... Please Wait')
        self.setCourses()
        print('{} courses found'.format(len(self.courses)))
        self.setCalender()

    def setCourses(self):
        driver = self.driver
        sleep(10)
        page = driver.find_element_by_css_selector('#main-content-inner > div')
        k = '#main-heading'
        body = driver.find_element_by_css_selector(k)
        body.click()
        body.send_keys(Keys.PAGE_DOWN)
        sleep(2)
        body.send_keys(Keys.PAGE_DOWN)
        sleep(2)

        self.codes = []
        self.names = []
        self.subcodes = []

        for item in page.find_elements_by_xpath('//*[@class="default-group term-"]'):
            courseid = item.find_element_by_css_selector(
                'bb-base-course-card > div').get_attribute('data-course-id')
            self.codes.append(courseid)
            self.names.append(item.find_element_by_css_selector(
                '#course-link-{} > h4'.format(courseid)).get_attribute('title'))
            self.subcodes.append(item.find_element_by_css_selector(
                '#course-list-course-{} > div.element-details.summary > div.multi-column-course-id'.format(courseid)).text)

        for item in page.find_elements_by_xpath('//*[@class="default-group term- last-item"]'):
            courseid = item.find_element_by_css_selector(
                'bb-base-course-card > div').get_attribute('data-course-id')
            self.codes.append(courseid)
            self.names.append(item.find_element_by_css_selector(
                '#course-link-{} > h4'.format(courseid)).get_attribute('title'))
            self.subcodes.append(item.find_element_by_css_selector(
                '#course-list-course-{} > div.element-details.summary > div.multi-column-course-id'.format(courseid)).text)

        # print(codes)
        # print(names)
        # print(subcodes)
        self.links = []
        for i in self.codes:
            self.links.append(
                'https://cuchd.blackboard.com/ultra/courses/'+i+'/outline')
        # print(links)

        for i in range(len(self.codes)):
            self.courses.append(
                (i+1, self.names[i], self.links[i], self.subcodes[i][:10]))

    def setCalender(self):
        self.weekdays = [('MON', []), ('TUE', []), ('WED', []),
                         ('THU', []), ('FRI', []), ('SAT', [])]

        for i in range(len(self.courses)):
            print('[' + str(self.courses[i][0]) + ']\t' +
                  str(self.courses[i][3]) + '\t' + str(self.courses[i][1]))

        print('Now set-up your daily calender.\tEnter the sub-codes as given above, enter 0 if you have no class or mid-day break.\nFor example if you have classes 1, 2, 3, break, 4 and 5 on the first day,\tEnter 1 2 3 0 4 5\n:')

        for k in range(6):
            restart = True
            while restart == True:
                restart = False
                userInpCal = list(
                    map(int, input('{}::'.format(self.weekdays[k][0])).split()))

                for _ in range(len(userInpCal)):
                    if userInpCal[_] == 0:
                        userInpCal[_] = None
                    if userInpCal[_] != None and userInpCal[_] > len(self.courses):
                        print("Error, you only have {} subjects!\nTry again!".format(
                            len(self.courses)))
                        restart = True
                        break

                for item in userInpCal:
                    if item != None:
                        couLink = self.courses[item-1][2]
                    else:
                        couLink = None
                    self.weekdays[k][1].append(couLink)

    def saveState(self):
        cred = './Data/.cred'

        with open(cred, 'w') as fileIn:
            fileIn.write("{}\n{}".format(self.username, self.password))

        courseFile = './Data/.courseFile'

        with open(courseFile, 'w') as fileIn:
            for i in range(len(self.codes)):
                fileIn.write("{} :: {} :: {} :: {}\n".format(
                    i+1, self.names[i], self.links[i], self.subcodes[i][:10]))

        calFile = './Data/.calFile'

        with open(calFile, 'w') as fileIn:
            for i in range(6):
                fileIn.write(str(self.weekdays[i][0]) + ' : [\n')
                for j in self.weekdays[i][1]:
                    fileIn.write(str(j)+'\n')
                fileIn.write("]\n\n")

    def begin(self, x, y):
        if x == 'Monday':
            self.bring(self.days[0], y)
        elif x == 'Tuesday':
            self.bring(self.days[1], y)
        elif x == 'Wednesday':
            self.bring(self.days[2], y)
        elif x == 'Thursday':
            self.bring(self.days[3], y)
        elif x == 'Friday':
            self.bring(self.days[4], y)
        elif x == 'Saturday':
            self.bring(self.days[5], y)
        else:
            print("It's a holiday, pal! Enjoy !")
            pass

    def bring(self, x, y):
        day = x
        driver = self.driver

        if y < 999:
            print("Hold ON !!!")
            sleep(((945 - y)//100)*3600 + ((945-y) % 100)*60)
            y = int(date.now().strftime("%H%M"))
            self.bring(x, y)
        elif y >= 1000 and y < 1045:
            t = 0
        elif y >= 1100 and y < 1145:
            t = 1
        elif y >= 1200 and y < 1245:
            t = 2
        elif y >= 1245 and y < 1345:
            t = 3
        elif y >= 1345 and y < 1430:
            t = 4
        elif y >= 1445 and y < 1530:
            t = 5
        elif y >= 1545 and y < 1630:
            t = 6
        elif y >= 1630:
            print("You're too late to handle the power of spinjitzu !!!")
        else:
            print('No class now... Please Wait !!')
            t = 0
            timeWaiting = (
                ((timestamps[t+1]//100)*60 + timestamps[t+1] % 100)*60 - ((y//100)*60 + y % 100)*60)
            sleep(timeWaiting)

        classno = 0

        while y < 1630:
            timeWaiting = (
                ((timestamps[t+1]//100)*60 + timestamps[t+1] % 100)*60 - ((y//100)*60 + y % 100)*60)

            if x[t] == None:
                print('No class right now... Waiting for ::\t' +
                      str(timeWaiting) + ' seconds !')
                sleep(timeWaiting)
                t += 1
                y = int(date.now().strftime("%H%M"))
                continue

            else:
                driver.get(x[t])
                print("\nClass from " +
                      str(timestamps[t]) + ' to ' + str(timestamps[t+1]))

            sleep(10)

            print("Getting Books !!!")
            driver.find_element_by_css_selector(
                '#sessions-list-dropdown').click()
            sleep(1)
            print("Getting in Class !!!")
            try:
                driver.find_element_by_xpath(
                    '/html/body/div[1]/div[2]/bb-base-layout/div/main/div[3]/div/div[3]/div/div/div/div[2]/div/div[2]/div[3]/div/div[2]/div[3]/aside/div[6]/div[2]/div[2]/div/div/ul/li[2]/a').click()
                sleep(45)
            except:
                print('No class or  BB error maybe !!!')

            driver.switch_to.window(driver.window_handles[-1])

            if classno == 0:
                print("Turning Mic On !")
                driver.find_element_by_css_selector(
                    "#dialog-description-audio > div.techcheck-controls.equal-buttons.buttons-2-md > button").click()
                sleep(10)
                print("Turning Video On !")
                driver.find_element_by_css_selector(
                    '#techcheck-video-ok-button').click()
                sleep(10)
                driver.find_element_by_css_selector(
                    '#announcement-modal-page-wrap > div > div.announcement-later-tutorial.ng-scope > button').click()
                sleep(1)
                try:
                    driver.find_element_by_css_selector(
                        '#tutorial-dialog-tutorials-menu-learn-about-tutorials-menu-close').click()
                    sleep(2)
                    driver.find_element_by_xpath(
                        '/html/body/div[1]/div[1]/main/bb-panel-open-control/div/button[1]').click()
                    sleep(1)
                    driver.find_element_by_xpath(
                        '/html/body/div[1]/div[1]/main/div[3]/section/div/div/ul/li/ul/li/bb-channel-list-item/button').click()
                    driver.find_element_by_xpath(
                        '//*[@id="channel-item-d74321ca-1af3-4008-a21a-6f38559f1924"]/span').click()
                    sleep(1)
                    timeWaiting -= 65
                except:
                    timeWaiting -= 60
            else:
                timeWaiting -= 20

            print("In class... Waiting for ::\t" +
                  str(timeWaiting) + ' seconds !')

            t += 1

            classno += 1
            sleep(timeWaiting)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            y = int(date.now().strftime("%H%M"))

        driver.quit()

    def bye(self):
        self.saveState()
        driver = self.driver
        driver.quit()
