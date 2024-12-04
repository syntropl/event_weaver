
import asana
from asana.rest import ApiException
from pprint import pprint

from asana_connection import get_asana_api_client


# https://github.com/Asana/python-asana/blob/master/docs/TasksApi.md

class AsanaTask:
    def __init__(self, data):
        self.gid = data['gid']
        self.name = data['name']
        self.assignee = data['assignee.name']
        self.due_on = data['due_on']
        self.notes = data['notes']

        self.is_separator = data['is_rendered_as_separator']


    def get_parameter(param_name:str)->str:
        param = self.data[param_name]
        if param:
            return param
