
# Android PyTorch Client with Flower

This is a PyTorch client interface running on Android that supports federated learning using the Flower federated learning framework. 

# Server Setup

[EC2 Setup Tutorial](https://docs.aws.amazon.com/efs/latest/ug/gs-step-one-create-ec2-resources.html)

For the Flower server, you can create a free Amazon Web Services EC2 instance running Ubuntu. The free tier service will work fine for the purposes of this setup. You can create a free account [here](https://portal.aws.amazon.com/billing/signup#/start). 

In order for the Android device to connect, you must authorize inbound traffic. If you are following the tutorial link above, step 6 of the setup is where you can allow inbound traffic.

![enter image description here](https://i.ibb.co/gJBRBvX/Screenshot-2021-07-12-233945.png)

After your server instance is up and running, SSH into your server. Also, make note of your <strong>public server IP address</strong>. We will need the IP for setting up the client on Android. You can find the IP address on your instance in the AWS EC2 dashboard.

![enter image description here](https://i.ibb.co/FD5RD1k/Screenshot-2021-07-19-232028.png)

Make sure python3 and pip3 are installed. Then, install the Flower python package.

    $ sudo apt update
    $ sudo apt install python3 python3-pip -y
    $ pip3 install --upgrade pip
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


Next, we need to install proot and ubuntu. Open up the Termux application. A terminal environment should appear on your phone. In the terminal, we need to change the repositories.

    $ termux-change-repo

![enter image description here](https://i.ibb.co/VB0yBP1/Screenshot-2021-07-19-222047.png)

Press <strong>Enter</strong> and change the repository to the Albatross mirror. Press <strong>Enter</strong>.

![enter image description here](https://i.ibb.co/YkLFXn5/Screenshot-2021-07-19-221935.png)
  ![enter image description here](https://i.ibb.co/xDHPGF2/Screenshot-2021-07-19-221950.png)

Now, we can update our repositories and install proot-distro from the terminal.
  
    $ pkg update
    $ pkg install proot-distro -y

After proot-distro is intalled, install and run the Ubuntu distro with the following commands.

    $ proot-distro install ubuntu-18.04
    $ proot-distro login ubuntu-18.04

![enter image description here](https://i.ibb.co/41rmKCS/Screenshot-2021-07-19-215542.png)

You should be greeted with a new root@localhost terminal. From here, we need to install python3, pip3, and git.

    $ apt update
    $ apt install python3 python3-pip git -y

Install the flwr and torch python packages, and clone the repository. This next step can take a while.

    $ pip3 install --upgrade pip
    $ pip3 install flwr torch torchvision
    $ git clone git://github.com/michael-j-cho/Flower-PyTorch-Android-Client.git

After cloning the git repository, we need to edit the client code and add the public server IP address from the server setup. Change directories and edit the <strong>client.py</strong> file.

    $ cd Flower-PyTorch-Android-Client
    $ nano client.py

![enter image description here](https://i.ibb.co/y6sJSW5/Screenshot-2021-07-19-230800.png)

Find the line "fl.client.start_numpy_client(....)" and enter the public ip address you obtained from the server setup. Exit and save the client.py file.

Finally, we can run the server and client to train our model.

# Training the Model

On the AWS instance, we can run the server with the following command:

    $ python3 server.py

Similarly, we can run the client from the Android device with:

    $ python3 client.py

You need two clients running in order for the federated training to begin. You can run the other client from any other device. Or, you can run both clients from the same Android device. However, this is not recommended as training may take awhile.

![enter image description here](https://i.ibb.co/KjtMmCk/Screenshot-2021-07-19-233138.png)

I hope you found this tutorial informative and helpful. Please let me know if anything needs clarification.
