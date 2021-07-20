
# Android PyTorch Client with Flower

This is an Android client that supports federated learning models based on PyTorch by using the Flower federated learning framework. 

# Server Setup

[EC2 Setup Tutorial](https://docs.aws.amazon.com/efs/latest/ug/gs-step-one-create-ec2-resources.html)

For the Flower server, you can create a free Amazon Web Services EC2 instance running Ubuntu. The free tier service will work fine for the purposes of this setup. You can create a free account [here](https://portal.aws.amazon.com/billing/signup#/start). 

In order for the Android device to connect, you must authorize inbound traffic. If you are following the tutorial link above, step 6 of the setup is where you can allow inbound traffic.

![enter image description here](https://i.ibb.co/gJBRBvX/Screenshot-2021-07-12-233945.png)

After your server instance is up and running, SSH into your server. Also, make note of your server IP address. We will need the IP for setting up the client on Android. Make sure python3 and pip3 are installed. Then, install the Flower python package.

    $ sudo apt update
    $ sudo apt install python3 python3-pip -y
    $ pip3 install flwr

Create a <span><strong>server.py</strong></span> file with your favorite text editor. Paste the following code into the server file and save.

    import flwr as fl
    fl.server.start_server(config={"num_rounds": 3})

This is a simple server configuration with all default values. More information can be found at the Flower website [here](https://flower.dev/docs/quickstart_pytorch.html#flower-server). 

The server should be all set. Continue to the Android client setup. Then, we should be able to run the client and server together.

# Client Setup

First, we need to setup a few things on the Android device in order to execute the client code. 

On your device, go to the Google Play Store and install the Termux application. You can also install Termux from many available apks found online. Termux is the terminal environment where we will be running our client code.

![enter image description here](https://i.ibb.co/MMHwYQQ/termux.png)

Next, we need to install proot and ubuntu. Open up the Termux application. A terminal environment should appear on your phone. In the terminal, update your package repositories and install proot with the following commands.

    $ pkg update
    $ pkg install proot-distro -y

Now, we can install and run the Ubuntu distro with the following commands.

    $ proot-distro install ubuntu-18.04
    $ proot-distro login ubuntu-18.04

![enter image description here](https://i.ibb.co/41rmKCS/Screenshot-2021-07-19-215542.png)

You should be greeted with a new root@localhost terminal. From here, we need to install the python packages and clone the repository. These next two commands can take a while, so please be patient.

    $ pip install flwr torch
    $ git clone https://github.com/michael-j-cho/Flower-PyTorch-Android-Client.git

After cloning the git repository, we need to edit the client code with the correct image directory and server IP address.

