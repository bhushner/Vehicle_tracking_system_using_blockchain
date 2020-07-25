import datetime
import json

import requests
from flask import render_template, redirect, request

from app import app
from collections import OrderedDict

import binascii

import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

import requests
from flask import Flask, jsonify, request, render_template



# The node with which our application interacts, there can be multiple
# such nodes as well.
CONNECTED_NODE_ADDRESS = "http://127.0.0.1:8000"


posts = []


def fetch_posts():
    """
    Function to fetch the chain from a blockchain node, parse the
    data and store it locally.
    """
    #for i in CONNECTED_NODE_ADDRESS:

    get_chain_address = "{}/chain".format(CONNECTED_NODE_ADDRESS)
    response = requests.get(get_chain_address)
    if response.status_code == 200:
        content = []
        chain = json.loads(response.content.decode('utf-8'))
        ##print("chain",chain)
        for block in chain["chain"]:
            for tx in block["transactions"]:
                timestamp = datetime.datetime.fromtimestamp(block["timestamp"])
                tx["timestamp"]=timestamp.strftime('%Y-%m-%d %H:%M:%S')
                tx["index"] = block["index"]
                tx["hash"] = block["hash"]
                tx["previous_hash"] = block["previous_hash"]
                content.append(tx)
        block=chain["chain"][0]
        tx={}
        tx["index"]=0
        tx["hash"]=block["hash"]
        tx["previous_hash"]="NA"
        tx["timestamp"]=block["timestamp"]
        print("GOT",block["timestamp"])
        tx["amount"]=0
        tx["author"]="NA"
        tx["v_type"]="NA"
        tx["content"]="NA"
        content.append(tx)
        global posts
        posts = sorted(content, key=lambda k: k['index'],
                    reverse=True)


@app.route('/')
def index():
    fetch_posts()
    
    return render_template('index.html',
                           title='BlockChain: Vehicle '
                                 'Tracking System ',
                           posts=posts,
                           node_address=CONNECTED_NODE_ADDRESS,
                           readable_time=timestamp_to_string)


@app.route('/wallet/new', methods=['GET'])
def new_wallet():
	random_gen = Crypto.Random.new().read
	private_address = RSA.generate(1024, random_gen)
	public_address = private_address.publickey()
	response = {
		'private_address': binascii.hexlify(private_address.exportKey(format='DER')).decode('ascii'),
		'public_address': binascii.hexlify(public_address.exportKey(format='DER')).decode('ascii')
	}

	return jsonify(response), 200


@app.route('/submit', methods=['POST'])
def submit_textarea():
    """
    Endpoint to create a new transaction via our application.
    """
    author = request.form["author"]
    buyer = request.form["buyer"]
    post_content = request.form["content"]
    s_public_key = request.form["s_public_key"]
    model = request.form["model"]
    v_type = request.form["v_type"]
    amount = request.form["amount"]

    post_object = {
        'author': author,
        'buyer' : buyer,
        'content': post_content,
        's_public_key': s_public_key,
        'model': model,
        'v_type' : v_type,
        'amount': amount
    }

    # Submit a transaction
    new_tx_address = "{}/new_transaction".format(CONNECTED_NODE_ADDRESS)

    requests.post(new_tx_address,
                  json=post_object,
                  headers={'Content-type': 'application/json'})

    return redirect('/')

@app.route('/transaction')
def transaction():
    return render_template('transaction.html',node_address=CONNECTED_NODE_ADDRESS,title='BlockChain: Vehicle '
                                 'Tracking System ')
@app.route('/wallet')
def wallet():
    return render_template('wallet.html',node_address=CONNECTED_NODE_ADDRESS,title='BlockChain: Vehicle '
                                 'Tracking System ')
@app.route('/get_chain')
def get_chain():
    fetch_posts()
    ##print("P",posts)
    return render_template('chain.html',posts=posts,readable_time=timestamp_to_string,node_address=CONNECTED_NODE_ADDRESS,title='BlockChain: Vehicle '
                                 'Tracking System ')

@app.route('/track')
def track():
    fetch_posts()
    #print("P",posts)
    return render_template('track.html',posts=posts,readable_time=timestamp_to_string,node_address=CONNECTED_NODE_ADDRESS,title='BlockChain: Vehicle '
                                 'Tracking System ')
def timestamp_to_string(epoch_time):
    return datetime.datetime.fromtimestamp(epoch_time).strftime('%H:%M')
