import os
from dotenv import load_dotenv

from clacks import listen_for_emails

def main():
    print("Will you be using an env file for important values? (y/n)")
    response = input()
    if response.lower() == 'y':
        load_dotenv()
        email_address = os.environ['GMAIL_ORIGIN_ADDRESS']
        gmail_app_key = os.environ['GMAIL_APP_KEY']
        phone_address = os.environ['RECEIVER_SMTP_ADDRESS']
        command_id_string = os.environ['COMMAND_IDENTIFIER']
        maps_api_key = os.environ['MAPS_API_KEY']


    if response.lower() == 'n':
        print("No sweat, let's grab some details we need to make this thing work.\nPlease enter your gmail address:")
        email_address = input()
        print("Please enter your gmail app key:")
        gmail_app_key = input()
        print("Please enter the SMTP address where you would like the instructions sent:")
        phone_address = input()
        print("Enter a command identifier string (you'll use it to mark messages intended for this tool):")
        command_id_string = input()
        print("Enter your google maps API key:")
        maps_api_key = input()

        if not all([email_address, gmail_app_key, phone_address, command_id_string, maps_api_key]):
            print("Oh no! You need all of the requested values to run this tool :(")
            return
        
    print("Great! That's everything. When you're ready to get your directions, just send a text to your email address with the following format:\n{YOUR COMMAND STRING} command: {STARTING LOCATION} --> {ENDING LOCATION}")
    listen_for_emails(email_address, phone_address, gmail_app_key, command_id_string, maps_api_key)    

if __name__ == "__main__":
    main()
