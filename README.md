Birthday Thanks
===============

Automate replies to all birthday wishes on facebook.

##Installation##

    git clone git@github.com:indradhanush/birthday-thanks.git
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt


##Usage##

* Get a valid Access Token from facebook.com
* Put it in ACCESS_TOKEN
* Put your full name in NAME. Note this must be same as the name in your facebook account.
* Put the START_TIME and END_TIME in seconds since epoch. See: http://www.epochconverter.com
* Run the following command:

    python thanks_bot.py
* Enjoy the magic! :)