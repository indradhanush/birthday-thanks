Birthday Thanks
===============

Automate replies to all birthday wishes on facebook.

##Installation##

    git clone git@github.com:indradhanush/birthday-thanks.git
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt


##Usage##

* Get a valid Access Token from [here](https://developers.facebook.com/tools/explorer/145634995501895/?method=GET&path=794489451%3Ffields%3Did%2Cname) and make sure you grant the following permissions:
  * `read_stream`
  * `read_insights`
  * `publish_actions`

* Put it in `ACCESS_TOKEN`
* Put your full name in `NAME`. Note this must be same as the name in your facebook account.
* Put the `START_TIME` and `END_TIME` in seconds since epoch. See: http://www.epochconverter.com
* Run the following command: `python thanks_bot.py`
* Be patient and enjoy the magic! :)
