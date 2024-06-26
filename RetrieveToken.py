import os
from xml.parsers.expat import ExpatError

import requests
import xmltodict
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

SISMEDIA_USER = os.getenv("SISMEDIA_USER")
SISMEDIA_PW = os.getenv("SISMEDIA_PASSWORD")
SISMEDIA_WEBSERVICE = os.getenv("SISMEDIA_WEBSERVICE")
MAX_TRIES = 3


def get_token_access(user, password, cont=0):
    headers = {'content-type': 'text/xml; charset=utf-8', 'SOAPAction': "http://localhost/Submedicionv2/GetTokenAccess"}

    body = """<?xml version="1.0" encoding="utf-8"?>
  <soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
    <soap12:Header>
      <oCabeceraSoapAcceso xmlns="http://localhost/Submedicionv2">
        <Usuario>""" + user + """</Usuario>
        <Password>""" + password + """</Password>
      </oCabeceraSoapAcceso>
    </soap12:Header>
    <soap12:Body>
      <GetTokenAccess xmlns="http://localhost/Submedicionv2" />
    </soap12:Body>
  </soap12:Envelope>
  """
    try:
        response = requests.post(SISMEDIA_WEBSERVICE, data=body, headers=headers)
        b = xmltodict.parse(response.content)
        c = b['soap:Envelope']['soap:Body']['GetTokenAccessResponse']['GetTokenAccessResult']['Token']
        return c
    except requests.exceptions.RequestException as e:
        if cont < MAX_TRIES:
            get_token_access(user, password, cont=cont + 1)
    except ExpatError as ex:
        print(ex)


def update_token_env():
    new_token = get_token_access(SISMEDIA_USER, SISMEDIA_PW)
    os.environ["SISMEDIA_TOKEN"] = new_token

    with open('.env', 'r') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if line.startswith('SISMEDIA_TOKEN'):
            lines[i] = f'SISMEDIA_TOKEN={new_token}\n'
            break
    else:
        lines.append(f'SISMEDIA_TOKEN={new_token}\n')

    with open('.env', 'w') as f:
        f.writelines(lines)
