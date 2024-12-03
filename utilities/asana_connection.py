import asana
from asana.rest import ApiException
from api_key_handler import get_api_key
from pprint import pprint

def get_asana_api_client():
    configuration = asana.Configuration()
    configuration.access_token = get_api_key("ASANA")
    return asana.ApiClient(configuration)

def verify_access() ->bool:
    api_client = get_asana_api_client()
    users_api = asana.UsersApi(api_client)
    user_gid = "me"
    opts = {'opt_fields': "email"}
    try:
        api_response = users_api.get_user(user_gid, opts)
        print(api_response)
        if "@" in api_response['email']:
            return True


    except ApiException as e:
        print(f"exception when calling asana UsersApi->get_user \n{e}")
    return False

if __name__ == "__main__":
    verify_access()