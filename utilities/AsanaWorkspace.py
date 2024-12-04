
import asana
from asana.rest import ApiException
from pprint import pprint

from asana_connection import get_asana_api_client
from AsanaProject import AsanaProject



class AsanaWorkspace:
    def __init__(self, data):
        self.gid = data['gid']
        self.name = data['name']
        self.data = data
    

        self.workspaces_api = asana.WorkspacesApi(get_asana_api_client())
        self.projects_api = asana.ProjectsApi(get_asana_api_client())
        self.project_objects = []
        self.project_objects_by_gid = {}
        self.project_objects_by_name = {}
        self.update_projects()





    def get_project(self, gid):
        return self.project_objects_by_gid[gid]

    def fetch_workspace_by_gid(self, gid: str):
        opts = {
            'opt_fields': "name"
        }
        try:
            print(f"Fetching Asana workspace with GID {gid}")
            api_response = self.workspaces_api.get_workspace(gid, opts)
            

            return api_response
        except ApiException as e:
            print(f"Exception when calling WorkspacesApi->get_workspace: {e}")

    def update_projects(self, archived=False):
        opts = {
            'limit': 100,
            'archived': archived,
            'opt_fields': '''
            name,
            gid,
            workspace.name
            created_at,
            current_status,
            current_status.author
            default_view,
            due_date,
            due_on,
            followers,
            followers.name,
            html_notes,
            members.name,
            notes,
            owner,
            path,
            permalink_url,
            privacy_setting,
            project_brief,
            uri
            '''
        }
        try:
            print(f"fetching projects for workspace {self.gid}")
            api_response = self.projects_api.get_projects_for_workspace(self.gid, opts)
            projects = list(api_response)
            for project in projects:
                obj = AsanaProject(project)
                self.project_objects.append(obj)
                self.project_objects_by_gid[obj.gid] =  obj
                self.project_objects_by_name[obj.name] = obj


        except ApiException as e:
            print(f"Exception when calling ProjectsApi->get_projects_for_workspace:\n{e}")
            return []
    
    def create_new_project(self, project_name: str):
        try:
            conflicting_project = self.project_objects_by_name[project_name]
            if conflicting_project:
                print(f'''creating "{project_name}" project cancelled. project with this name, already exists (gid: {conflicting_project.gid})''')
                return
        except Exception as e:
            pass
        
        opts = {'opt_fields': 'created_at'}
        body = {'data': {'name': project_name}}
        try:
            print(f"Creating project {project_name} at workspace {self.gid}")
            api_response = self.projects_api.create_project_for_workspace(body, self.gid, opts)
            return api_response
        except ApiException as e:
            print(f"Exception when calling ProjectsApi->create_project:\n{e}")
    def delete_project(self, project_gid):
        api_response = self.projects_api.delete_project(project_gid)
        return api_response
    