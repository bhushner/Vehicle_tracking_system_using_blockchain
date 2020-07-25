# Vehicle_tracking_system_using_blockchain
A simple application project for vehicle tracking  using a blockchain technology  in Python.
# Vehicle_tracking_system_using_blockchain

A simple project for developing a blockchain application from scratch in Python.

## What is blockchain? How it is implemented? And how it works?

Please read the [step-by-step implementation tutorial](https://www.ibm.com/developerworks/cloud/library/cl-develop-blockchain-app-in-python/index.html) to get your answers :)

## Instructions to run

1. Clone/ download the project
2. Install python3
3. Start Virtual environment
4. Install the dependencies (From requirements.txt file)

```sh
$ pip install -r requirements.txt
```

5. Start a blockchain node server
## Run Scripts from scripts folder by changing the path of virtual environment 
## OR
```sh
# Windows users can follow this: https://flask.palletsprojects.com/en/1.1.x/cli/#application-discovery
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

You can use the following cURL requests to register the nodes at port `8001` and `8002` with the already running `8000`.

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

This will make the node at port 8000 aware of the nodes at port 8001 and 8002, and make the newer nodes sync the chain with the node 8000, so that they are able to actively participate in the mining process post registration.

To update the node with which the frontend application syncs (default is localhost port 8000), change `CONNECTED_NODE_ADDRESS` field in the [views.py](/app/views.py) file.

Once you do all this, you can run the application, create transactions (post messages via the web inteface), and once you mine the transactions, all the nodes in the network will update the chain. The chain of the nodes can also be inspected by inovking `/chain` endpoint using cURL.

```sh
$ curl -X GET http://localhost:8001/display_chain
$ curl -X GET http://localhost:8002/display_chain
```
