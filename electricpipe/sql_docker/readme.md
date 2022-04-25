# Setting up the MS-SQL docker container

I'm tearing down the container all the time since I don't want to pay to have it up, but I've saved its config in a storage account that I persist.

I'm also going to make a local version of the container that I can test my local function against so I don't have to go through big push deploy sequences while testing.

## One time start for the remote container

Once the container instance is up and running, find the container group in the Azure portal, head over to the container and bring up a shell.

Open the sql prompt with ```/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P <your_password>```
execute the commands in ```setup.sql``` in this folder.