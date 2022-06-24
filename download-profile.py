import time
import os
from sys import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from gologin import GoLogin
import sys
from selenium.webdriver.chrome import service
from selenium_stealth import stealth
from py4j.java_gateway import JavaGateway
import subprocess
import shutil

arrArgv = sys.argv
if len(arrArgv) > 3:
	idProfile = str(arrArgv[1])
	nameProfile = str(arrArgv[2])
	strToken = str(arrArgv[3])
	print("IdProfile: "+idProfile+" nameProfile: "+nameProfile+" strToken: "+strToken)
	gateway = JavaGateway()
	objJava_Application = gateway.entry_point

	number_portFree = objJava_Application.GetPortNotUse()
	gl = GoLogin({
	"token": strToken,
	"profile_id": idProfile,
	"local": False,
	"credentials_enable_service": False,
    "NumberPortTool": number_portFree,
	})

	dirProject = os.path.abspath(os.curdir)
	chrome_driver_path = dirProject+"\\chromedriver.exe"

	for x in range(2):
		debugger_address = gl.start()

		#print("Start Profile: "+debugger_address+" "+gl.port)
		subprocess.run([dirProject+"\\HideProcess.exe", nameProfile+" - New Tab"])
		# if x ==0:

			# time.sleep(2)
			# subprocess.run([dirProject+"\\CloseProcess.exe", nameProfile+" - New Tab"])
		if x == 1:

			dirProject_Browser = os.path.abspath(os.curdir)+"\\TaoProfileGologin\\ProfileGologin\\gologin_"+idProfile
			xJson = {
			  'id': idProfile,
			  'path': dirProject_Browser,
			  'Cmd': '--user-data-dir="'+dirProject_Browser+'" --lang=en-US --disable-encryption --restore-last-session --font-masking-mode=2 --flag-switches-begin --flag-switches-end',
			  'ProfileName': nameProfile
			}
			print(xJson)

			objJava_Application.AddProfile(str(xJson))


		# '''
		try:
			chrome_options = Options()
			chrome_options.add_experimental_option("debuggerAddress", debugger_address)
			myService = service.Service(chrome_driver_path)
			drivers = webdriver.Chrome(service=myService, options=chrome_options)
			stealth(drivers)
			urlCheck =""
			if x == 0:
			    urlCheck = "https://iphey.com"
			else:
			    urlCheck = "https://www.google.com/"

			drivers.get(urlCheck)
			drivers.close()
			gl.stop()
			if x == 1:
				dirProject_Browser = os.path.abspath(os.curdir)+"\\TaoProfileGologin\\ProfileGologin\\gologin_"+idProfile
				dirproject_save = os.path.abspath(os.curdir)+"\\TaoProfileGologin\\ProfileSave\\gologin_"+idProfile
				shutil.copytree(dirProject_Browser, dirproject_save)
		except Exception as e:
		    try:
		        gl.stop()
		    except:
		        print("Error Gl Stop")

		    print("Error")
		    objJava_Application.KillProces("0", nameProfile)
		    x = x - 1
		    continue
		# '''

	gl.delete(idProfile)
	print("Del Profile: "+idProfile)

