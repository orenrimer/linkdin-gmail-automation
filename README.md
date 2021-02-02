# linkdin-job-alert-automation


A short script to check your job alerts from LinkedIn using Python and Selenium Webdriver, connecting to Gmail REST API.<br>
This script uses the Gmail API to get all your recent unread messages. then it will check if you got a new LinkedIn job alert mail, 
if so it will get the link from the mail and will open a browser window using selenium so you can start your job hunt.


# How To run 

install the required packages from the requirements.txt using:
```python
pip install -r requirements.txt
```

You need to download the 'credentials.json' file from here: https://developers.google.com/gmail/api/quickstart/python <br>
and clciking "Enable the Gmail API"

In the first run, you will need to give the app permissions, then token.pickle will be created automatically.
