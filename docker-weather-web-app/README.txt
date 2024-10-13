_____________________________________Weather_App_____________________________________

This Weather Application retrieves and displays weather data for specified locations. 
It uses the OpenWeatherMap API to get weather forecasts and stores the results in a database. 
The application can run in two different environments: Docker and locally on your machine.
Provides a web interface to display the weather data.
When running in Docker Enviroment, it uses docker-compose to manage both the app container and the db container 


_____________________________________Project_Tree_____________________________________
├── app.py
├── setup.py
├── database.py
├── data_processing.py
├── api_key_handler.py
├── error_handler.py
├── docker-compose.yaml
├── Dockerfile
├── requirements.txt
├── templates
│   └── index.html
├── tools
│   ├── print_docker_db.py
│   └── printer_local_db.py
└── weather.db # Will create it self if needed, after first local run


_____________________________________.env_file_____________________________________
Should include the followign :
MY_API_KEY='weather_server_api_key'
MONGO_URI='mongodb://mongo-db:27017/weather_db'
MONGO_LOCAL_URI='mongodb://localhost:27017/weather_db'

In the docker-compose.yml file, the MongoDB port is mapped to 27017, which is MongoDB deafult port.

Note: If port 27017 is already in use by another service on the local machine, 
you will need to change the port number in both MONGO_LOCAL_URI and the docker-compose.yml file.

MONGO_LOCAL_URI='mongodb://localhost:<new_port>/weather_db'

docker-compose.yaml :
ports:
  - "<new_port>:27017"


_____________________________________Databases_____________________________________

For Docker Environments : mongodb volume at /var/lib/docker/volumes/pythonproject3_mongo-data
For Local Environments : sqlite3 weather.db file at path/to/the/project

_____________________________________Requirements_____________________________________

Flask
requests
python-dotenv
pymongo
Flask-PyMongo

_____________________________________Run_in_dockers_____________________________________
1. cd path/to/the/project
2. sudo docker-compose up --build -d
3. access via http://localhost:9000

____View_MongoDB____
1.sudo docker exec -it mongo-db mongo
2.use weather_db
3.db.daily_summaries.find().pretty()
____________________

_____________________________________Run_locally_____________________________________
1. cd path/to/the/project
2. python app.py
3. access via http://localhost:5000
____View_weather.db____
1.sqlite3 weather.db
2.SELECT * FROM daily_summaries;
_____________________________________Tools_____________________________________
This folder includes two printing functions that allow you to print data from the databases without the need for SSH access.



