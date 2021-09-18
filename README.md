# Personal finance management system
A RESTful service that allows to store info about users (also to create, update, delete it), their transactions and perform operations under these transactions (create new ones, update info about particular transaction).
## How to launch?
1. Clone the repository
2. In the root directory it is enough to use docker-compose:
<code>sudo docker-compose up</code>

## How to use?
See <code>openapi.yml</code> to get description of endpoints, input and output schema and descripiton of status codes

## How to change configuration?
see <code>.env</code> file, where there are definitions of variables using in the project: -PostgreSQL credentials to connect to database. We may also change the port on which the server will listen requests
