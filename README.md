# Boilerplate for Python Flask App from Scratch

Boilerplate how to get started using the Flask framework. 
- [x] create new virtual env and install the necessary packages and get a basic Hello World Application running in our browser. 
- [ ] prepare HTML for application 
- [ ] adding styling


## 1. Creating virtual environment for new project.

Virtual Environments in Python allow us to keep project-specific dependencies in a separate place than our global site-packages. This is extremely useful when you have different versions of packages for different projects.


##### Folder to keep all environments on my computer:

```
/Environments
```

##### 1.1 To create new env: 

```
virtualenv {nameOfProject}
```

In case, when you want create new, virtual env with specific version of Python:

```
virtualenv -p /usr/bin/python2.6 {nameOfProject}
```

##### 1.2. Activate Python env:

```
source {nameOfNewProject}/bin/activate
```

##### 1.3. Install new packages into local env:


```
pip install {nameOfPackage}

pip install flask
```

If you want to go back to being in the global env:

```
deactivate
```
Prompt with name of project no longer shows up.


If you want delete virtual env:

```
rm -rf {nameOfProject}
```

To enlist all packages:


```
pip list
```

You can also use your global site packahes within virtual Python environment.

Freezing is a process where pip reads the versions of all installed packages in a local virtual environment and then produces a text file with the package version for each python package specified. By convention, it's named requirements. txt .

```
pip freeze --local >environment.txt
```

To make sure you got all packages:

```
cat environment.txt
```

You get list of all packages with versions.


In case, you want install those packages from environment.txt in next project:

```
pip install -r requirements.txt
```



## 2. Creating app.py 

Create new folder for your application and file app.py, starting with example from the documentation:

```
from flask import Flask, escape, request

app = Flask(__name__)

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

```

##### 2.1. Join virtual environment with Python app's file:

Before running application you need to set an environment variable to the file, that you want to be flask application.

In line command of your virtual Python environment go to your project's folder and type in:

```
export FLASK_APP=app.py

```
![picture](images/set_folder.png)


On the port 5000 it will show Hello world.




## Forms and User Input.

```
pip install flask-wtf

```