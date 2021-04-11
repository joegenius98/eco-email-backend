# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gmail_quickstart]
from __future__ import print_function
import sys
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import email
import base64
import random
import json

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


# def get_children(email_obj):
#     return email_object.get_payload()


# def allElementsAreTypeStr(a_list):
#     return sum(type(ele) == str for ele in a_list) == len(a_list)


# def convertToStrMsgs(emailObjList):
#     toRet = emailObjList[:]

#     currEmail = None

#     while not allElementsAreTypeStr(toRet):
#         currEmail = toRet[0]

#         if type(currEmail) != str:
#             toRet += get_children(toRet[0])
#             del toRet[0]


def get_multipart_messages(service, user_id, msg_id):

    # toRet = []
    try:
        message = service.users().messages().get(
            userId=user_id, id=msg_id, format='raw').execute()  # "raw" means byte format-based, and we need to decode

        msg_raw = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))

        # print(msg_raw)

        msg_str = email.message_from_bytes(msg_raw)

        # print(msg_str)

        content_type = msg_str.get_content_maintype()

        if content_type == "multipart":
            # main_msg = msg_str.get_payload()[0]

            # # print("this is the main message object:")
            # # print(main_msg)

            # # # part 1 is plain text, part 2 is html text
            # # print("get payload of this main message")
            # # print(main_msg.get_payload())

            # part1, part2 = main_msg.get_payload()

            # print("This is the message body: ")
            # print(part1.get_payload())
            return [part_msg.get_payload() for part_msg in msg_str.get_payload()]

        else:
            return msg_str.get_payload()

    except ValueError as vE:
        print(f"An error occurred: {vE}")
        print(
            "Safely ignore this error if you see 'too many values to unpack (expected 2)'")
        return main_msg.get_payload()


def search_messages(service, user_id, search_string):
    try:
        # retrieve the email message ids based on a search query

        # If there are no search results, it looks like this: {'resultSizeEstimate': 0}

        search_ids = service.users().messages().list(
            userId=user_id, q=search_string).execute()

        # print(search_ids)

        # handle the case that there are no search results
        number_results = search_ids['resultSizeEstimate']

        final_list = []

        if number_results > 0:
            message_id_list = search_ids['messages']

            # search_ids has this format:
            '''
            {'messages': [{'id': ..., 'threadId': ...}, 
            ...,
            {'id': ..., 'threadId': ...}],
            'resultSizeEstimate': #}
            '''

            for ids in message_id_list:
                # ids has format {'id': ..., 'threadId'...}
                final_list.append(ids['id'])

            # print(final_list)

            return final_list

        else:  # let the user know there were no search results and return an empty string
            print("There were no results for your search. ")
            print("Returning an empty string...")
            return ""

    except:
        print(f"An error occurred: {sys.exc_info()[0]}")


def get_service():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    return service


if __name__ == '__main__':
    # main()
    service = get_service()
    # print(service)

    # search_query = input("Tell me something to search for: ")

    amazon_search_query = "Amazon.com"
    flight_search_query = "Your trip confirmation"

    amazon_msg_ids = search_messages(
        service=service, user_id='me', search_string=amazon_search_query)

    flight_msg_ids = search_messages(
        service=service, user_id='me', search_string=flight_search_query)

    if amazon_msg_ids and flight_msg_ids:
        # print(get_message(service=service,
        #       user_id='me', msg_id=random.choice(message_ids)))

        # rand_msg_id = random.choice(message_ids)
        # print("Your message id is: " + rand_msg_id)

        # multipart_msgs = get_multipart_messages(service=service,
        #                                         user_id='me', msg_id=rand_msg_id)

        # python_json = {"content": None}

        # python_json["content"] = {f"part_{i}": multipart_msgs[i]
        #                           for i in range(len(multipart_msgs))}

        python_json = {"First Name": "",
                       "Last Name": "", "email": "", "env_impact": {}}

        python_json["First Name"] = "Sam"
        python_json["Last Name"] = "Pies"
        python_json["email"] = "sampieslovestheearth@gmail.com"
        python_json["env_impact"]["carbon_ton"] = len(flight_msg_ids)
        python_json["env_impact"]["plastic_ton"] = len(amazon_msg_ids)

        # json_formatted_str = json.dumps(python_json, indent=2)
        # print(json_formatted_str)

        with open("output/impact.json", "w") as outfile:
            json.dump(python_json, outfile)


# [END gmail_quickstart]


'''
Sources:
1. https://youtu.be/vgk7Yio-GQw
2. https://www.journaldev.com/33302/python-pretty-print-json
3. https://www.w3schools.com/python/ref_random_choices.asp
'''
