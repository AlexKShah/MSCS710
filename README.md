# Limón : Linux Monitor
## Alex Shah & Steven Guarino
### MSCS 710 Spring 2019

<img src="img/block.png" height="561px" width="930px" align="center">

## Requirements:
Ubuntu LTS (18.04+)

Docker (17+)

docker-compose (1.13+)

## Installation
* Clone the repository on the machine you want to monitor:

      git clone https://github.com/AlexKShah/MSCS710.git; cd MSCS710;

* Setup:

      sudo apt update && sudo apt install -y docker docker-compose

      ln -s /proc /path/to/repo/proc
* Build:

      sudo docker-compose up --build

* Monitor

     Navigate to `machineIP:5000` in a browser

## Configuration
* Modify parameters like how often to gather metrics at:
    
      limon/flask/sys_poll.yml
