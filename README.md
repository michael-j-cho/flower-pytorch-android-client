# Android PyTorch Client with Flower

This is an Android client that supports federated learning models based on PyTorch by using the Flower federated learning framework. 

# Server Setup

For the Flower server, you can create a free Amazon Web Services EC2 instance running Ubuntu. The free tier service will work fine for the purposes of this setup. You can create a free account [here](https://portal.aws.amazon.com/billing/signup#/start). In order for the Android device to connect, you must authorize inbound traffic. 

![enter image description here](https://i.ibb.co/gJBRBvX/Screenshot-2021-07-12-233945.png)

After your server instance is up and running. You can setup the Flower server. Make sure python3 and pip3 are installed. Then, install the Flower python package.

    $ sudo apt update
    $ sudo apt install python3 python3-pip -y
    $ pip3 install flwr

Create a <span><strong>server.py</strong></span> file with the following code in it.

    import flwr as fl
    fl.server.start_server(config={"num_rounds": 3})

This is a simple server configuration with all default values. More information can be found at the Flower website [here](https://flower.dev/docs/quickstart_pytorch.html#flower-server). 

When you are ready to start the server, you can run it with the following command:

    $ python3 server.py

# Client Setup


