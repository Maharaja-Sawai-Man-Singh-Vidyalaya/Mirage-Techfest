<p align="center">
    <img src="https://i.ibb.co/wz97TGd/mirage-logo-modified.png" width="270" height="270"/>
</p>

### ➜ Mirage Hostable Bot

The new mirage bot, the one customisable, and the one you can use however you like. 

- Customisable
- Fast
- Easy to use

### ➜ Support
Join our support & community discord server for any queries or support in general!

[![](https://i.ibb.co/Y3kq58Z/Untitled.png)](https://discord.gg/cHYWdK5GNt)

### ➜ Help Us
Become a patron, by simply clicking on this button **very appreciated!**:

[![](https://c5.patreon.com/external/logo/become_a_patron_button.png)](https://www.patreon.com/hyenabot)

### ➜ How to setup the bot

> For any doubts here, contact S1D#3953 please.
> Follow the steps given below

Step 1: Fork & Clone the repository

```sh
$ git clone link-to-my-forked-repository.git miragebot
$ cd miragebot
```

Step 2: Setup virtual environment
This can simply be done by doing the following:

```sh
$ virtualenv venv # Linux/mac

$ py -m venv venv # Windows
```

Step 3: Activating virtual environment and setting up the dependencies

```sh
$ source ./venv/bin/activate  # Linux/mac # from root dir

$ venv\Scripts\activate.bat # Windows
```
Now our virtual env should be activated, time to install the packages & databases.
```sh
$ pip install -U -r requirements.txt  # Linux/mac

$ py -m pip install -U -r requirements.txt # Windows
```

Step 4: Configuring the config file

* Copy the 'config_example.yml' file to a file with the name of 'config.yml'
* Now change the configuration values according to your needs

Step 5: Configuring the env file

* Copy the 'src/.env.example' file to a file with the name of 'src/.env'
* Change the environment variables accordingly

Step 6: Running the Bot

```sh
$ cd src # change directory
$ python3 __main__.py # run the bot
```