#Generate Requirement File:
`pip freeze > requirements.txt`

#Install libs from requirement file:
`pip install -r requirements.txt`

## instruções de como instalar um venv em um ambiente linux (Ubuntu 20.04)

https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-programming-environment-on-an-ubuntu-20-04-server-pt

para rodar no linux tive que utilizar _virtualenv_ ao invés de _venv_
entao rodei os comandos:

- instalar virtualenv `sudo apt install python3-virtualenv`
- criar virtualenv `virtualenv -p python3 [env_name]`

export FLASK_APP=hello
