# trackfolio

Are you a little kooky like me, and like to track stuff? Then this is the app for you. 
Track any type of event or activity so you can see frequency of your events. 
For example: How often you change HVAC filter, get haircuts, cut your cat's nails, clean your espresso machine.

## 📖 Installation
```
$ git clone https://github.com/ecumike/trackfolio.git
$ cd trackfolio
```


### Setup

```
$ python -m venv .venv
$ source .venv/bin/activate

(.venv) $ pip install -r requirements.txt
(.venv) $ ./manage.py migrate
(.venv) $ ./manage.py createsuperuser
(.venv) $ ./manage.py runserver

# Load the site at http://127.0.0.1:8000
```

### Sample data

```
# Generate a sample data set of events and event logs
(.venv) $ ./manage.py generate_sample_events

# Clear all events and logs
(.venv) $ ./manage.py clear_events
```

### ⭐️ Support
Give a ⭐️  if this project helped you!

### License
[Apache 2 license - Free to use and modify](LICENSE)

