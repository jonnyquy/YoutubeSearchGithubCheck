Local $sServiceName = "sshd"
Local $oShell = ObjCreate("shell.application")
$runable = $oShell.IsServiceRunning($sServiceName)
If $runable == False Then
	Do
		$iResult = RunWait(@ComSpec & ' /c net start ' & $sServiceName, '', @SW_HIDE)
		Sleep(100)
	Until $oShell.IsServiceRunning($sServiceName)
EndIf
