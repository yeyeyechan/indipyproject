cd C:\dev/indipyproject/process

sudo taskkill /fi "imagename eq python.exe" /F

sudo python autoLogin.py

timeout /t 15

sudo python SC_new.py
sudo python SK_new.py
sudo python SP.py
sudo python realTimeConclusion.py
sudo python RealTimeAccount.py
sudo python monitoring_report.py