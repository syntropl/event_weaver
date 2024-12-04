
import asana
from asana.rest import ApiException
from pprint import pprint

from asana_connection import get_asana_api_client
from AsanaUser import AsanaUser




def test():
    user = AsanaUser()
    testing_ground = user.get_workspace("1208893838024861")
    testing_ground.create_new_project("something")
    for workspace in user.workspace_objects:
        for project in workspace.project_objects:
            print(f"{project.gid}  {project.name} ")

if __name__ == "__main__":
    test()

