import json
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import yagmail
import keyring

from matplotlib import pyplot as plt
import numpy as np

def JSONParse(fN):
    with open(fN) as file:
        data = json.load(file)

    #Read data
    #Source https://www.freecodecamp.org/news/python-read-json-file-how-to-load-json-from-a-file-and-parse-dumps/
    co2TN = data["env_impact"]["carbon_ton"]
    plastTN = data["env_impact"]["plastic_ton"]
    totFP = co2TN + plastTN
    percCo2Tot = co2TN/totFP
    percPlastTot = plastTN/totFP

    #Pie Chart
    vars = ('Tons of Carbon', 'Tons of Plastic')
    data2 = [co2TN, plastTN]

    fig = plt.figure(figsize =(10,7))
    plt.pie(data2, labels = vars)

    plt.savefig('test.jpg')

    # Advice
    if percCo2Tot < percPlastTot :
        advice = """You should reduce your plastic purchases.
        Do you want the turtles to die at YOUR hands?
        Do you want the sea to wipe out civilization Because of YOU?
        Then do something about it ;)
        """
    else :
        advice = """You should travel less.
        Do you want your city to become an uninhabitable wasteland because of YOU?
        Do you want the sea to wipe out civilization at YOUR hands?
        Then do something about it ;)
        """

    #Sending Email
    #Source https://realpython.com/python-send-email/
    sender_email = "eco.email.automated@gmail.com"
    password = "AutoEcoEmail123"
    receiver_email = data["email"]
    keyring.set_password('yagmail', sender_email, password)
    filename = "test.jpg"

    text = f"""Your carbon footprint is {totFP} tons of carbon.
    Your carbon footprint due to transportation and plastic consumption is {co2TN} and {plastTN} respectively.
    {advice}"""

    yag = yagmail.SMTP("eco.email.automated@gmail.com")
    yag.send(
        to=receiver_email,
        subject="Your Carbon Footprint",
        contents=text,
        attachments=filename,
    )