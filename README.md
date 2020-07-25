# Vehicle_tracking_system_using_blockchain
A simple project for developing a blockchain application from scratch in Python. Vehicle Tracking System using block chain project will maintain the
security of the vehicles by tracking it with the help of block-chain.

## What is blockchain? 
The blockchain is a decentralized distributed database of immutable records. The technology was discovered with the invention of Bitcoins
(the first cryptocurrency). It’s a trusted approach and there are a lot of companies in the present scenario which are using it. As everything is secure, and because it’s an open source approach, it can easily be trusted in the long run.

## Instructions to run

1. Clone/ download the project
2. Install python3
3. Start Virtual environment
4. Install the flask and its dependencies (From requirements.txt file)

```sh
$ pip install -r requirements.txt
```

5. Start a blockchain node server
## Run Scripts from scripts folder (edit the path of your virtual environment)
## OR
```sh
$ export FLASK_APP=node_server.py
$ flask run --port 8000
```

One instance of our blockchain node is now up and running at port 8000.

Run the application on a different terminal session,

```sh
$ python run_app.py
```

The application should be up and running at [http://localhost:5000](http://localhost:5000).


To play around by spinning off multiple custom nodes, use the `register_with/` endpoint to register a new node. 
##view script connect_node.sh OR
Here's a sample scenario that you might wanna try,

```sh
# Make sure you set the FLASK_APP environment variable to node_server.py before running these nodes
# already running
$ flask run --port 8000 &
# spinning up new nodes
$ flask run --port 8001 &
$ flask run --port 8002 &
```

You can use the following curl requests to register the nodes at port `8001` and `8002` with the already running `8000`.

```sh
curl -X POST \
  http://127.0.0.1:8001/register_with \
  -H 'Content-Type: application/json' \
  -d '{"node_address": "http://127.0.0.1:8000"}'
```

```sh
curl -X POST \
  http://127.0.0.1:8002/register_with \
  -H 'Content-Type: application/json' \
  -d '{"node_address": "http://127.0.0.1:8000"}'
```

All the other nodes in the network will update the chain. The chain of the nodes can also be inspected by invoking `/display_chain` endpoint using curl.

```sh
$ curl -X GET http://localhost:8001/display_chain
$ curl -X GET http://localhost:8002/display_chain
```
