ECHO ON
REM A batch script to execute a Python script
py -m pip install --upgrade pip3
pip3 install -r requirements.txt
pip3 install bs4
pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
py extractor.py
PAUSE