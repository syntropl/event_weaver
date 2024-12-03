import os
from pathlib import Path
from dotenv import load_dotenv, set_key

from langchain_community.llms import OpenAI 

import asana_connection as asana_connection

ENV_FILE = Path('.') / '.env'
load_dotenv(dotenv_path=ENV_FILE, override=True)

    
def set_api_key(vendor: str, key: str):
    """
    Sets the vendor API key after verification and stores it in the .env file.

    """
    try:
        vendor = str.upper(vendor)

        # Store the API key in the .env file
        print(f'''\nsetting api key for {vendor} as environment variable''')
        set_key(str(ENV_FILE), f"{vendor}_API_KEY", key)
        print('''reading api key from env''')
        load_dotenv(dotenv_path=ENV_FILE, override=True)

        if (os.getenv(f"{vendor}_API_KEY")==key):
            
            print("\nAPI KEY IS SET")
        else:
            print('\n\nERROR: key NOT SAVED to env')

    except Exception as e:
        print(f"\n\nERROR: Failed to set API key. {str(e)}")
 
def get_api_key(vendor:str):
    load_dotenv(dotenv_path=ENV_FILE, override=True)
    vendor = str.upper(vendor)
    key = os.getenv(f"{vendor}_API_KEY")
    return key


def print_api_key(vendor:str, masked=False):
    key = get_api_key(vendor)
    if key is None:
        print("API key not found in environment variables.")
    
    if masked:
        masked_key = f"{key[:10]}{'*' * (len(key) - 20)}{key[-10:]}"
        print(masked_key)
    else:
        print(key)
    
def verify_openai_api_key(key: str) -> bool:
    try:
        load_dotenv(dotenv_path=ENV_FILE, override=True)
        
        llm = OpenAI(openai_api_key=key)
        test_prompt = '''"Respond only with a word exactly 11 characters long. interlinked."'''

        response_text = llm.invoke(test_prompt).strip().strip('.')

        print(f'''verifying api key...\n\n\n
              TEST PROMPT:\n{test_prompt}\n\n
              RESPONSE: \n{response_text}''' )
     
        # TODO add 2 retries 
        if len(response_text) == 11:
            print("openai api connection verified")
            return True
        else:
            print(f"\n\nTEST FAILED:\nResponse length is {len(response_text)} instead of 11.\n")
            return False
    except Exception as e:
        print(f"Error during API call: {e}")
        return False
    
def ensure_openai_api_key_is_verified() -> bool:
    """
    Retrieves the API key from the .env file and verifies its validity.
    Returns True if valid, False otherwise.

    Returns:
        bool: True if the API key from .env is valid, False otherwise.
    """
    load_dotenv(dotenv_path=ENV_FILE, override=True)
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("API key is not set in .env file.")
            return False
        if verify_openai_api_key(api_key):
            return True
        else:
            print("ERROR: OPENAI_API_KEY from .env is invalid.")
            return False
    except Exception as e:
        print(f"ERROR: Failed to verify API key from environment. {str(e)}")
        return False

def mask_api_key(api_key: str) -> str:

    if len(api_key) <= 4:
        return "*" * len(api_key)
    else:
        return "*" * (len(api_key) - 4) + api_key[-4:]

def cli_vendor_setup(vendor:str):
    vendor = str.upper(vendor)
    key_shortcut = ""
    match vendor:
        case "OPENAI":
            key_shortcut = "get your api key here: https://platform.openai.com/api-keys"
        case "ASANA":
            key_shortcut = "get personal token at: https://app.asana.com/0/my-apps"
        case "GOOGLE":
            key_shortcut = "to get the key follow instructions here: https://support.google.com/googleapi/answer/6158862"

    key = input(f"input your {vendor} api key\n({key_shortcut})\ninput your key and press enter\n>")
    set_api_key(vendor, key)
    print_api_key(vendor, masked=False)
    print("\n")
    
    if vendor == "OPENAI":
        ensure_openai_api_key_is_verified()

api_helpstring = '''

COMMAND           DESCRIPTION
-------------------------------------------------
set_oai           to set new openai api key
set_asana         to set new asana key
set_google        to set new google api key

print_oai
print_asana
print_google


'''

def main():
    vendors = ["OPENAI", "ASANA", "GOOGLE"]
    for vendor in vendors:
        if not os.getenv(f"{vendor}_API_KEY"):
            cli_vendor_setup(vendor) 
    print("\n\n your api keys:\n")
    for vendor in vendors:
        print(vendor)
        print_api_key(vendor, masked=True)
        print("\n")
    ensure_openai_api_key_is_verified()

    should_continue = True
    print(api_helpstring)
    while should_continue:

        user_input = input("type command to manage api keys\n>")
        match user_input:
            case "set_oai":
                set_api_key("OPENAI",input("input your openai api key\n>"))
            case "set asana":
                set_api_key("ASANA",input("input your asana api key\n>"))
            case "set_google":
                set_api_key("GOOGLE",input("input your gooogle api key\n>"))
            case "print_oai":
                print_api_key("OPENAI", masked=False)
            case "print_asana":
                print_api_key("ASANA", masked=False)
            case "print_google":
                print_api_key("GOOGLE", masked=False)
            case "test_oai":
                ensure_openai_api_key_is_verified()
            case "test_asana":
                asana_connection.verify_access()
            case "test_google":
                print("      not implemented :(")
            case _:
                break








    
