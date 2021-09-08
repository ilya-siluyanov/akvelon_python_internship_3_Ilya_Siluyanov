# Personal finance management system
A RESTful service that allows to store info about users, their transactions and perform operations under these transactions.
## How to launch?
It is enough to use docker-compose in root directory:
<code>sudo docker-compose up --build</code>

## How to use?
See <code>openapi.yml</code> to get description of endpoints, input and output schema and descripiton of status codes

## How to change configuration?
see <code>.env</code> file, where there are definitions of variables using in the project: -PostgreSQL credentials to connect to database. We may also change the port on which the server will listen requests
