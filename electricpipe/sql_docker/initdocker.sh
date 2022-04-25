#!/bin/bash
# clean up old stuff to start
sudo docker container stop mssql
sudo docker container rm mssql
sudo docker volume rm mssqlvol
sudo docker volume create mssqlvol
sudo docker run \
  -e "ACCEPT_EULA=Y" \
  -e "SA_PASSWORD=W3akP@ssword" \
  -p 1433:1433 \
  -v mssqlvol:/var/opt/mssql \
  --name mssql \
  -d mcr.microsoft.com/mssql/server:2019-latest

sudo docker cp setup.sql mssql:/var/opt/mssql/setup.sql
#run the setup script to create the DB and the schema in the DB
#do this in a loop because the timing for when the SQL instance is ready is indeterminate
for i in {1..50};
do
    sudo docker exec -it mssql /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P "W3akP@ssword" -d master -i /var/opt/mssql/setup.sql
    if [ $? -eq 0 ]
    then
        echo "setup.sql completed"
        break
    else
        echo "not ready yet..."
        sleep 1
    fi
done
