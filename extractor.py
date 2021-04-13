from __future__ import print_function
import re
import os.path
import urllib.request as urlb
from datetime import datetime
from bs4.element import Comment
from bs4 import BeautifulSoup as bs
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import settings

def read_structural_elements(elements):

    # Reading the Structural Elements of Google Docs    

    """Recurses through a list of Structural Elements to read a document's text where text may be
        in nested elements.

        Args:
            elements: a list of Structural Elements.
    """
    text = ''

    for value in elements:
        if 'paragraph' in value:
            elements1 = value.get('startIndex')
            elements2 = value.get('endIndex')
    return elements1,elements2


def write_file(text,now):

    # Writing the Code into a file

    with open(now , "a", encoding="utf-8-sig") as writer:
        writer.write(text)

def read_file(file):

    # Reading the contents of the file

    with open(file , "r", encoding="utf-8-sig") as reader:
        return(reader.read())


def read_url(url,now):

    # Article Extraction of the Website

    d = urlb.urlopen(url)
    data = d.read()
    soup = bs(data, 'lxml')
    for data in soup(['header','style', 'script','footer','aside','span','iframe']):
        # Remove tags
        data.decompose()

    test_texts = ''
    title = soup.title.get_text()
    write_file('\n############################################\n\n' + title + '\n\n',now)
    texts = soup.findAll(text=True)

    for ele in texts:
        if (ele.parent.name in ['header','nav','head','title', 'meta', '[document]','span','footer','img','i']):
            continue
        elif (ele.parent.name in ['p','a','h1','h2','h3','h4','h5','h6']):
            test_texts += ele + '\n'
        elif (ele.parent.name == 'li'):
            test_texts += '\t' + ele + '\n'
        elif (ele.parent.name in  ['ui','ol']):
            test_texts += '\t' + ele + '\n'



    article_data = re.sub(r'\n+', '\n', test_texts).strip()
    print(article_data)
    
    write_file(article_data,now)
    return article_data


def main():
    nowtimestamp = int(datetime.timestamp(datetime.now()))
    now = ("{:%Y_%m_%d_%H_%M_%S}".format(datetime.now()))

    # print(now)
    time = datetime.fromtimestamp(nowtimestamp)
    settings.init()
    service = build('docs', 'v1', credentials=settings.creds)
    start,end = read_structural_elements(settings.doc_content)
    print("The Start Index = ", start)
    print("The End Index = ", end)
    if end!=2:
        requests = [
        {
            'deleteContentRange': {
                'range': {
                    'startIndex': 1,
                    'endIndex': (end-1),
                }

            }

        },
        ]
        service.documents().batchUpdate(documentId=settings.DOCUMENT_ID, body={'requests': requests}).execute()
    links = read_file("links")
    links = links.split('\n')
    for idx in range(len(links),0,-1):
        link = links[idx-1]
        data = read_url(link,now)
        heading = ('Article ' + str(idx) + '\n')
        requests = [
        {'insertText': 
            {'location':
                {'index': 1},
            'text': (data + '\n\n\n')
            }
        }
        ]
        service = build('docs', 'v1', credentials=settings.creds)
        service.documents().batchUpdate(documentId=settings.DOCUMENT_ID, body={'requests': requests}).execute()

        requests = [
        {"updateTextStyle":
            {"range":
                {"startIndex":1,"endIndex":(1 + len(data))},
            "textStyle":
                {"bold":False},
            "fields":"bold"
            }
        }
        ]
        service = build('docs', 'v1', credentials=settings.creds)
        service.documents().batchUpdate(documentId=settings.DOCUMENT_ID, body={'requests': requests}).execute()

        requests = [
        {'insertText': 
            {'location':
                {'index': 1},
            'text': (heading + '\n\n')
            }
        }
        ]
        service = build('docs', 'v1', credentials=settings.creds)
        service.documents().batchUpdate(documentId=settings.DOCUMENT_ID, body={'requests': requests}).execute()


        
        requests = [
        {"updateTextStyle":
            {"range":
                {"startIndex":1,"endIndex":(1 + len(heading) - 1)},
            "textStyle":
                {"bold":True},
            "fields":"bold"
            }
        }
        ]
        service = build('docs', 'v1', credentials=settings.creds)
        service.documents().batchUpdate(documentId=settings.DOCUMENT_ID, body={'requests': requests}).execute()
    print("File Created at :", time.ctime())

if __name__ == '__main__':
    main()