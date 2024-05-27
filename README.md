# httpRshell
reverse shell via http requests/response
### about :
httpRshell.py is a Windows/Linux reverse shell payload generator and handler that abuses the http protocol to establish a reverse shell. it offers generating a one liner payloads in 3 different scripting languages ( python , bash , powershell )

### installatino :
clone the github repo
```
git clone https://github.com/o-sec/httpRshell.git
```
cd to httpRshell directory 
```
cd httpRshell
```
change httpRshell.py file permission
```
chmod +x httpRshell.py
```
### usage :
 httpRshell.py <SERVER-HOST> <SERVER-PORT> <PAYLOAD-TYPE>
e.g :

generating a python payload and start a listener :
httpRshell.py  192.168.1.12 8080 py
generating a powershell payload and start a listener :
httpRshell.py 192.168.1.12 8080 ps
generating a bash payload and start a listener :
httpRshell.py 192.168.1.12 8080 sh

note : 
the bash payload require curl to be installed on the target machine !.
also the powershell payload is for windows machines and could be used on linux by simply edit the first line in the payload_sample.ps1 file by replacing the "$env:username" with "(whoami)" , and replace the payload.ps1 start "powershell.exe" with "pwsh".

### disclaimer :
i am not responsable for whatever you do with this tool !

