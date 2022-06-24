from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from gologin import GoLogin
from selenium_stealth import stealth
from selenium.webdriver.chrome import service
import random
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import subprocess
from py4j.java_gateway import JavaGateway
import sys
from sys import platform
import shutil

class CreateProfile:
    def __init__(self, token, profilename, idprofile = ""):
            self.token = token
            self.profilename = profilename
            self.idprofile = idprofile


    def Create(self):
            gl = GoLogin({
                "token": self.token,
                })
            profile_id = gl.create({
                    "name": self.profilename,
                    "os": 'win',
            }, random.randint(2, 999));
            self.idprofile = profile_id

class LocalAuto:
    def __init__(self, token, idprofile, profilename,  gl_service,  objJava_Application = None, gmail = "", password = "", mail_kp = ""):
        self.token = token
        self.idprofile = idprofile
        self.profilename = profilename
        self.gl_service = gl_service
        self.objJava_Application = objJava_Application
        self.gmail = gmail
        self.password = password
        self.mail_kp = mail_kp


    def LoginGmail(self):
        dirProject = os.path.abspath(os.curdir)
        chrome_path = dirProject+"\\chromedriver.exe"

        subprocess.run([dirProject+"\\HideProcess.exe", self.profilename+" - New Tab"])
        driver = None
        urlCheck = ""
        while True:
            try:
                debug = self.gl_service.start()
                chrome_options = Options()
                chrome_options.add_experimental_option("debuggerAddress", debug)
                myService = service.Service(chrome_path)
                driver = webdriver.Chrome(service=myService, options=chrome_options)
                stealth(driver)
                if self.gmail != "":
                    urlCheck = "https://accounts.google.com/signin/v2/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&service=mail&sacu=1&rip=1&flowName=GlifWebSignIn&flowEntry=ServiceLogin"
                else:
                    urlCheck = "https://www.google.com"
                driver.set_page_load_timeout(60)
                driver.set_script_timeout(60)
                driver.get(urlCheck)

            except Exception as e:
                try:
                    self.gl_service.stop()
                    time.sleep(1)

                except Exception as ex:
                    print("Close Service: "+str(ex))

                print("Close Process:"+str(e))
                objJava_Application.KillProces("0", self.profilename)
                continue



            if self.gmail != "":
                get_curent_url = ""
                c_o = 0
                while True:
                    try:
                        print("checkout url")
                        get_curent_url = driver.current_url
                        if get_curent_url is not None:
                            if get_curent_url != "":
                                break
                        if c_o >=4:
                            driver.get(urlCheck)
                    except:
                        c_o = c_o + 1
                        time.sleep(1)
                        continue

                elmUsn = None
                while True:
                    try:
                        xpath_usn = '//input[contains(@autocomplete, "username")]'
                        elmUsn = driver.find_element(By.XPATH, xpath_usn)
                        if elmUsn is not None:
                            elmUsn.send_keys(self.gmail)
                            elmUsn.send_keys(Keys.RETURN)
                    except:
                        elmUsn = None
                        time.sleep(1)
                        print("Error SendMail")
                    else:
                        break

                this_curent = ""
                while True:
                    try:
                        this_curent = driver.current_url
                        xpath_pass = '//input[contains(@name, "password")]'
                        elmPassword = driver.find_element(By.XPATH, xpath_pass)
                        if elmPassword is not None:
                            elmPassword.send_keys(self.password)
                            elmPassword.send_keys(Keys.ENTER)
                            time.sleep(2)
                            print("Thoát")
                            break
                    except:
                        elmPassword= None
                        time.sleep(1)
                        print("Error SendPass")

                xpath_error_pass = '//div[contains(@class, "OyEIQ uSvLId")]'
                elSaiMatKhau = None

                try:
                    elSaiMatKhau = driver.find_element(By.XPATH, xpath_error_pass)
                    print("elSaiMatKhau not none")
                except:
                    elSaiMatKhau = None
                    print("elSaiMatKhau is none")

                if elSaiMatKhau == None:
                    get_curent_url = ""
                    while True:
                        try:
                            get_curent_url = driver.current_url
                            if get_curent_url != this_curent:
                                break
                        except:
                            print("Error Get Current")
                    print(get_curent_url)
                    if "https://mail.google.com/mail/u/0/#inbox" in get_curent_url:
                        try:
                            js_click = '''
                                document.querySelector("div[class='VfPpkd-Jh9lGc']").click()
                            '''
                            driver.execute_script(js_click)
                        except:
                            print("not now = False")

                        print("Login Success")
                        break
                    else:
                        #kiểm tra mail khôi phục, xác minh email
                        xpath_Mail_khoiphuc = '//form[contains(@method,"post")]//div[contains(@class, "lCoei YZVTmd SmR8")]'
                        WebDriverWait(driver, 3).until(EC.visibility_of_all_elements_located((By.XPATH, xpath_Mail_khoiphuc)))
                        print("Wait xpath_Mail_khoiphuc")
                        this_curent = ""
                        #time.sleep(2)
                        elmXacMinh = list()
                        try:
                            elmXacMinh = driver.find_elements(By.XPATH, xpath_Mail_khoiphuc)
                        except:
                            elmXacMinh = list()

                        if len(elmXacMinh) >= 3:
                            #vị trí button nhập mail khôi phục 1
                            print("len elmXacMinh > 0")
                            for q in elmXacMinh:
                                print(q.text)

                            elmXacMinh[1].click()
                            time.sleep(0.5)
                            elmInputMail_kp = None
                            while True:
                                try:
                                    xpath_mailkp = '//input[contains(@id, "knowledge-preregistered-email-response")]'
                                    elmInputMail_kp = driver.find_element(By.XPATH, xpath_mailkp)
                                    this_curent = driver.current_url
                                except:
                                    elmInputMail_kp = None
                                    print("Error elmInputMail_kp")
                                if elmInputMail_kp is not None:
                                    print("Sendkey  gEmail mail_kp")
                                    elmInputMail_kp.send_keys(self.mail_kp)
                                    elmInputMail_kp.send_keys(Keys.ENTER)
                                    time.sleep(0.5)
                                    break
                        else:

                            try:
                                driver.close()
                                driver.quit()
                            except:
                                print("Error driver.close")
                            try:
                                self.gl_service.stop()
                            except:
                                pass
                            break
                            print("elmxacminh < 3")

                        get_curent_url = ""
                        while True:
                            try:
                                get_curent_url = driver.current_url
                                if get_curent_url != this_curent:
                                    break
                            except:
                                print("Error Get Current")
                        if "https://mail.google.com/mail/u/0/#inbox" in get_curent_url:
                            print("Login Gmail Success")
                        else:
                            #bắt nhập số điện thoại hoặc vấn đề <>
                            print("Login Gmail Error")

                        print("len elmXacMinh:"+str(len(elmXacMinh)))

                        try:
                            driver.close()
                            driver.quit()
                        except:
                            print("Error driver.close")
                        try:
                            self.gl_service.stop()
                        except:
                            pass
                        break
                else:
                    try:
                        driver.close()
                        driver.quit()
                    except:
                        print("Error driver.close")
                    try:
                        self.gl_service.stop()
                    except:
                        pass
                    break

            else:
                #không login = gmail nếu gmail = rỗng
                try:
                    driver.close()
                    driver.quit()
                except:
                    print("Error driver.close")
                try:
                    self.gl_service.stop()
                except:
                    pass
                #exit
                print("Exit")
                break

    def SaveProfile(self):
        dirProject = os.path.abspath(os.curdir)
        chrome_path = dirProject+"\\chromedriver.exe"

        driver = None
        boocheck = True
        while True:

            if boocheck:
                dirProject_Browser = os.path.abspath(os.curdir)+"\\TaoProfileGologin\\ProfileGologin\\gologin_"+self.idprofile
                xJson = {
                  'id': self.idprofile,
                  'path': dirProject_Browser,
                  'Cmd': '--user-data-dir="'+dirProject_Browser+'" --lang=en-US --disable-encryption --restore-last-session --font-masking-mode=2 --flag-switches-begin --flag-switches-end',
                  'ProfileName': self.profilename
                }
                print(xJson)
                objJava_Application.AddProfile(str(xJson))
                boocheck = False

            try:
                debug = self.gl_service.start()
                chrome_options = Options()
                chrome_options.add_experimental_option("debuggerAddress", debug)
                myService = service.Service(chrome_path)
                driver = webdriver.Chrome(service=myService, options=chrome_options)
                stealth(driver)
                urlCheck = "https://www.youtube.com"
                driver.set_page_load_timeout(60)
                driver.set_script_timeout(60)
                driver.get(urlCheck)

                driver.close()
                driver.quit()
                self.gl_service.stop()
                dirProject_Browser = os.path.abspath(os.curdir)+"\\TaoProfileGologin\\ProfileGologin\\gologin_"+self.idprofile
                dirproject_save = os.path.abspath(os.curdir)+"\\TaoProfileGologin\\ProfileSave\\gologin_"+self.idprofile
                shutil.copytree(dirProject_Browser, dirproject_save)
            except Exception as ex:
                try:
                    self.gl_service.stop()
                    time.sleep(1)
                except Exception as e:
                    print("Error: gl_service"+str(e))

                print("Close Process: "+str(ex))
                objJava_Application.KillProces("0", self.profilename)
                continue


            break

        try:
           	self.gl_service.delete(self.idprofile)
            #print("Del Profile: "+self.idprofile)
        except Exception as e:
            print("Error Delprofile "+str(e))



if __name__ == '__main__':
    arrArgv = sys.argv
    if len(arrArgv) > 2:
##        token ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2MmI0Mjk4NTZlNGExZjU5OWI3NDVlYzgiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2MmI0MjlhNGNhYWVkZjY4MzAwZWM5N2IifQ.9Yc5smlMUpVbqB2-fHVsI8iV1iNeeItNuFk3l56iqDc"
##        profilename = "profile 4"
##        arrArgv = [3, token, profilename]
        token= ""
        profilename = ""
        gmail = ""
        password = ""
        mail_kp = ""
        if len(arrArgv) == 3:
            token = str(arrArgv[1])
            profilename = str(arrArgv[2])
        if len(arrArgv) == 6:
            token = str(arrArgv[1])
            profilename = str(arrArgv[2])
            gmail = str(arrArgv[3])
            password = str(arrArgv[4])
            mail_kp = str(arrArgv[5])

       	gateway = JavaGateway()
        objJava_Application = gateway.entry_point
        objProfile = CreateProfile(token, profilename)
        createProfile = objProfile.Create()
        idProfile =objProfile.idprofile
        print(idProfile)
        number_portFree = objJava_Application.GetPortNotUse()
        gl_service = GoLogin({
            "token": token,
            "profile_id": idProfile,
            "local": False,
            "credentials_enable_service": False,
            "NumberPortTool": number_portFree,
            })
        gl_auto = LocalAuto(token, idProfile, objProfile.profilename, gl_service, objJava_Application, gmail = gmail, password = password, mail_kp=mail_kp)
        gl_auto.LoginGmail()
        gl_auto.SaveProfile()



