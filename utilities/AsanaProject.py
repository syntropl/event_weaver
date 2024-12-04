
import asana
from asana.rest import ApiException
from pprint import pprint

from asana_connection import get_asana_api_client
from AsanaTask import AsanaTask

class AsanaProject:
    def __init__(self, data):
        self.projects_api = asana.ProjectsApi(get_asana_api_client())
        self.name = data['name']
        self.gid = data['gid']
        self.data = data




    def rename(self, project_gid:str, new_name:str):
        opts = {'opt_fields': '''created_at,current_status.modified_at,workspace.name'''}
        body = {"data":{
            'name':new_name
        }}
        old_name = ""
        try:
            print(f"renaming project {old_name} to {new_name}")
            api_response = self.projects_api.update_project(body, project_gid, opts)
            return api_response
        except ApiException as e:
            print(f"Exception when calling ProjectsApi->update_project:\n{e}")

        return

    def get_tasks():
        pass