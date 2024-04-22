# Notes on docker-compose for airflow
##### run the db init command first, then the up command to ensure a clean database
docker-compose up -d airflow-init
docker-compose up -d

##### When updaing dependencies add to the reqirements.txt then re-run build to update the image
docker-compose build

##### full clean up command 
docker compose down --volumes --rmi all
