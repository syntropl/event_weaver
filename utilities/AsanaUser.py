import asana
from asana.rest import ApiException
from asana_connection import get_asana_api_client
from pprint import pprint


from AsanaWorkspace import AsanaWorkspace





class AsanaUser:
    def __init__(self):
        self.workspaces_api = asana.WorkspacesApi(get_asana_api_client())
        self.workspace_objects = []
        self.workspace_objects_by_gid = {}
        self.update_workspaces()

    
    def get_workspace(self, gid):
        try:
            workspace = self.workspace_objects_by_gid[gid]
            return workspace
        except Exception as e:
            print(f"Error: workspace not found {e}")
        

    def update_workspaces(self):
        opts = {
            'limit': 50,
            'opt_fields': "name"
        }
        try:
            print("fetching all asana workspaces")
            api_response = self.workspaces_api.get_workspaces(opts)
            workspaces = list(api_response)
            if not workspaces:
                print("no workspaces returned by asana api")
            for workspace in workspaces:

                obj = AsanaWorkspace(workspace)
                self.workspace_objects.append(obj)
                self.workspace_objects_by_gid[obj.gid] = obj
                print(f"{obj.gid} {obj.name}")

        
        except ApiException as e:
            print(f"Exception when calling WorkspacesApi->get_workspaces:\n{e}")