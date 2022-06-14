#download chrome
powershell -command "Invoke-WebRequest 'https://dl.google.com/tag/s/appguid%3D%7B8A69D345-D564-463C-AFF1-A69D9E530F96%7D%26iid%3D%7B8D058EAC-2B8B-B976-922A-186B7289394B%7D%26lang%3Dvi%26browser%3D4%26usagestats%3D1%26appname%3DGoogle%2520Chrome%26needsadmin%3Dprefers%26ap%3Dx64-stable-statsdef_1%26brand%3DCHBD%26installdataindex%3Dempty/update2/installers/ChromeSetup.exe' -OutFile 'ChromeSetup.exe'"
start ChromeSetup.exe
#download openssh
powershell -command "Invoke-WebRequest 'https://github.com/PowerShell/Win32-OpenSSH/releases/download/v8.9.1.0p1-Beta/OpenSSH-Win32.zip' -OutFile 'OpenSSH-Win32.zip'"
