# Setup :

Most of these steps must be followed in order, don't try to parallelize them if you don't know what it is.

## python
- `python -m venv env` (validate when your IDE asks to change for virtual environment)
- `.\env\Scripts\activate` (Win) / `source env/bin/activate` (Mac/Lin)
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`

## docker
Install docker for your OS.
In the terminal, change diectory to the docker folder : `cd docker`</br>
Launch docker for the first time : `docker-compose up -d` (might need admin/sudo) (very long downloads)</br>
Go back to the project folder : `cd ..`

## postgres through pgAdmin
Docker needs to be launched for this step.

### Getting the IP address of the postgres server
Use the command `docker inpect postgres` (might need admin/sudo).
You only need to save the "IPAddress" value at the very bottom of the result (ex : "172.18.0.5").

### Connecting to pgAdmin
Go to http://localhost:8081 in your browser and login with username `coi-scd@outlook.com` and password `password`.

### Registering postgres server
In the pgAdmin interface, right-click on "Servers" (top left) to register your postgres server.</br>
The server name can be anything, but the "connection" tab needs important information :
- Host name/address : the IP Address found earlier
- Port : `5432`
- Username : `postgres`
- Password : `password`
You might need to register the server again if you want to change its configuration, only the IP Address will change in this case.

### Creating required database
Once the server registered and connected, right-click on "Databases" to create a new database, its name must be `RealTime`, no extra information should be necessary.

### Populate database with tables
First, check if the python virtual environment is activated, there should be written `(env)` at the start of the last terminal line.</br>
If the environment is not activated, refer to the Setup/python part of this doc.</br>
Launch the python script to create the tables : `python command/pgsql_init.py`.</br>
The output in terminal should be :
```logs
$ python command/pgsql_init.py 
Reseting tables...
Tables reset !
('GlobalData', 'timestamp')
('GlobalData', 'motor_on')
('RoomCommand', 'timestamp')
('RoomCommand', 'room_id')
('RoomCommand', 'detect')
('RoomCommand', 'variate')
('RoomCommand', 'variation')
('RoomCommand', 'is_on')
('RoomData', 'timestamp')
('RoomData', 'room_id')
('RoomData', 'is_on')
('RoomData', 'luminosity')
```

## rabbitMQ
There is nothing to setup.

## nifi
Does not work.

# Modification :

Don't forget to always `git pull <remote> <branch>` before editing the code to make sure you're working on the latest version.
Then use : `git add -A`, `git commit -m "<commit message>"`, `git push -u <remote> <branch>`.