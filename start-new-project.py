# This is a sample Python script.
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import re
import subprocess

# Prepare your detail information
# Fill your project name
project_name = input("Enter Project Name : ")
project_name = re.sub('[^a-zA-Z0-9 \n\.]', '', project_name).replace(" ", "-").lower()
print("Your Project Name : ", project_name)

# Fill your Modules
modules = input("Enter Modules / Services (use comma separator for more than 1 services) : ")
modules = modules.replace(" ", "")
print("Your Modules/Services : ", modules)

# Core Data
project_folder = "{0}/".format(project_name)
activate_virtual_env = "source env/bin/activate &&"


# Setup Project
def setup_project():
    # Remove & Create folder project
    subprocess.run(["rm", "-rf", project_name])
    subprocess.run(["mkdir", project_name])
    # Create Services/Modules directory
    subprocess.call("mkdir services", cwd=project_folder, shell=True)
    subprocess.run(["cp", "project-format/__init__.py", "{0}/services".format(project_folder)])
    # Copy requirements file into your Project
    subprocess.run(["cp", "project-format/requirements.txt", project_name])
    # Create virtual environment
    subprocess.run(["python3", "-m", "venv", "env"], cwd=project_folder)
    # Install Dependencies or Libraries
    subprocess.call("{0} python -m pip install —-upgrade pip".format(activate_virtual_env), cwd=project_folder, shell=True)
    subprocess.call("{0} pip install django-admin".format(activate_virtual_env), cwd=project_folder, shell=True)
    subprocess.call("{0} pip install django".format(activate_virtual_env), cwd=project_folder, shell=True)
    subprocess.call("{0} pip install -r requirements.txt".format(activate_virtual_env), cwd=project_folder, shell=True)
    subprocess.call("{0} django-admin startproject main".format(activate_virtual_env), cwd=project_folder, shell=True)

    # Change Project Structure
    subprocess.call("cp -R {0}/main/main/* {0}/main".format(project_name), shell=True)
    subprocess.call("cp -R {0}/main/manage.py {0}".format(project_name), shell=True)
    subprocess.call("rm -rf {0}/main/main".format(project_name), shell=True)
    subprocess.call("rm -rf {0}/main/manage.py".format(project_name), shell=True)

    # Create each Services/Modules directory
    module_lists = modules.split(",")
    for module in module_lists:
        subprocess.call("mkdir services/{0}".format(module.lower()), cwd=project_folder, shell=True)


def setup_services():
    apps = []
    for module in modules.split(","):
        module = module.lower()
        apps.append("services.{0}".format(module))
        subprocess.call("{0} python manage.py startapp {1} ./services/{1}".format(activate_virtual_env, module), cwd=project_folder, shell=True)


setup_project()
setup_services()
