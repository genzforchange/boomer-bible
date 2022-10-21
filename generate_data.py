from __future__ import print_function

import json

from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/documents.readonly']
SERVICE_ACCOUNT_FILE = 'credentials.json'
# Set doc ID, as found at `https://docs.google.com/document/d/YOUR_DOC_ID/edit`
DOCUMENT_ID = '1jVpcE2baS8s5liSWR6cFQMzhXDu4e-zzPUu_nbueMPk'

creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('docs', 'v1', credentials=creds)

def read_paragraph_element(element):
    """Returns the text in the given ParagraphElement.

        Args:
            element: a ParagraphElement from a Google Doc.
    """
    text_run = element.get('textRun')
    if not text_run:
        return ''
    return text_run.get('content')

def get_line(value):
    res = ""
    elems = value.get('paragraph').get('elements')
    for elem in elems:
        res += read_paragraph_element(elem)
    return res.strip()

def make_dict(elements):
    d = []
    curr_name = ""
    curr_topic = ""
    curr_event = ""
    in_desc = False
    for value in elements:
        if 'paragraph' not in value:
            continue
        if value['paragraph']['paragraphStyle']['namedStyleType'] == 'HEADING_1':
            in_desc = False
            curr_name = get_line(value)
            d.append({'name': curr_name, 'topics':[]})
        elif value['paragraph']['paragraphStyle']['namedStyleType'] == 'HEADING_2':
            in_desc = False
            curr_topic = get_line(value)
            d[-1]['topics'].append({'name': curr_topic, 'events': []})
        elif value['paragraph']['paragraphStyle']['namedStyleType'] == 'HEADING_3':
            in_desc = True
            curr_event = get_line(value)
            d[-1]['topics'][-1]['events'].append({'date': curr_event, 'description': []})
        else:
            val = get_line(value)
            if in_desc and val:
                d[-1]['topics'][-1]['events'][-1]['description'].append(val)
        
    return d

def execute():
    # Retrieve the documents contents from the Docs service.
    doc = service.documents().get(documentId=DOCUMENT_ID).execute()
    doc_content = doc.get('body').get('content')
    res = make_dict(doc_content)
    with open('data.json', 'w') as file:
        json.dump(res, file, indent=4)
