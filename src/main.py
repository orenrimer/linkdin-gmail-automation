import base64
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from selenium.webdriver import Firefox
import pickle
import os.path


# If modifying these scopes, delete the file token.pickle.
# You need to download the 'credentials.json' file from here: https://developers.google.com/gmail/api/quickstart/python
# In thee first run, you will need to give the app permissions, then token.pickle will be created automatically.


SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def check_new_email(max_results=10):
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    results = service.users().messages().list(userId='me', labelIds=['INBOX'],
                                              maxResults=max_results, q='category:primary is:unread ',
                                              ).execute()
    messages = results.get('messages', [])

    if not messages:
        print('No New messages found.')
        return 
    else:
        for message in messages:
            message_id = message['id']
            message = service.users().messages().get(userId='me', id=message_id, format='full').execute()
            headers = message['payload']['headers']

            for header in headers:
                if header['name'] == 'From':
                    if header['value'] == 'LinkedIn Job Alerts <jobalerts-noreply@linkedin.com>':
                        print("Found New Job Alert Mail")
                        service.users().messages().modify(
                            userId='me', id=message_id,
                            body={'addLabelIds': [],
                                  'removeLabelIds': ['UNREAD']}
                        ).execute()
                        link = ""
                        msg_body = message['payload']['parts'][0]['body']['data']
                        msg_string = base64.urlsafe_b64decode(msg_body.encode("ASCII")).decode("utf-8")
                        lines = msg_string.split('\r\n')
                        for line in lines:
                            if 'See all jobs on LinkedIn:' in line:
                                link = line.split('//')[1]
                        return link
    return None


class Bot:
    def __init__(self, jobs_link):
        self.driver = Firefox()
        self.driver.maximize_window()
        self.driver.get("https://" + jobs_link)
        self.driver.implicitly_wait(5)

    def login(self, password):
        self.driver.find_element_by_id('password').send_keys(password)
        self.driver.find_element_by_xpath("//button[@type='submit']").click()



if __name__ == '__main__':
    password = ""  # Your linkedin password
    jobs_link = check_new_email()
    if jobs_link:
        b = Bot(jobs_link)
        b.login(password)
        print("Opened Job Alert page")
    else:
        raise Exception("Filed to extract link from message.")