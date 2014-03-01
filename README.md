[DzLibs](http://dzlibs.io/) Project [![Build Status](https://travis-ci.org/01walid/dzlibs.png?branch=master)](https://travis-ci.org/01walid/dzlibs)
===========================

A community-driven Algerian index of reusable assets and libraries. A web app and a set of RESTful APIs to provide a platform for Algerian developers and designers to share reusable resources (Classes, Libraries, Vector files..etc) and easily access them. 

**For instance**:

You can share/find the XML or JSON of the 48 Algerian Wilayas instead of recreating it every time you need it for your next awesome web/mobile/desktop app. the same goes for the database of the Train/Bus timetable of your city, the Algeria SVG map, the Vector file of [Maqam Echahid](http://en.wikipedia.org/wiki/Maqam_Echahid), and countless other examples, these are *reusable* items we can share for the public good, from developers/designers to developers/designers, for a better Algeria.

The APIs part is mostly for developers, it consists of :

* Making **some** of these assets accessible via http(s) requests, for instance: a mobile developer (especially now that we've got the 3G network) could make a GET to `api.dzlibs.io/wilayas/23` that returns the name of the Wilaya and other on-demand information (e.g. its prayer times).
* pushing for a kind of **standardized** ways to share public data among Algerian developers and different DZ organizations.

These are **just examples**, what we can do and share is countless. we just need to unit, and do the same as our ancestors did, the **tweeza** of the Algerian web. boosting the IT industry is our shared duty, and for that we need to **share** and think of ourselves as contributors rather than as competitors.

# Installation

Before walking through the following steps, please make sure you have [MongoDB](http://www.mongodb.org/) installed on your system.

Start mongodb as a service/daemon, for Ubuntu:
`[sudo] service mongodb start`

For systemd-based distributions:
`[sudo] systemctl start mongodb`

If you want it to be started automatically after system reboot:
`[sudo] systemctl enable mongodb`

Then, it's highly recommended to install [Pip](https://pypi.python.org/pypi/pip) then [Virtual env](https://pypi.python.org/pypi/virtualenv) 
first, respectively.

For Pip under Ubuntu, try: `apt-get install python-pip` or search the web in case the name of the package has changed. Make sure that the pip package is for Python2 not Python3.

Once Pip installed, you can install Virtualenv by running:

```bash
$ [sudo] pip install virtualenv
```

Then download the source code, and do the following:

```bash
$ cd path/to/the/downloaded/source
# create a virtual isolated python2 environment
$ virtualenv venv # or it may be called virtualenv-2 or something similar...
# activate the new python environment
$ source venv/bin/activate
# now install the project requirements
$ pip install -r requirements.txt
# after downloading launch the project by running:
$ cd tweeza
# setup initial categories and licenses
$ python manage.py setup
$ python manage.py runserver
```

If all goes well, you should see something like this in your Terminal:

```bash
 * Running on http://127.0.0.1:5000/
 * Restarting with reloader
```

Then open the following URL in your browser to test the app: http://127.0.0.1:5000.

Now, follow these steps if you want customize the config file to your needs:
* under the `tweeza/instance` folder, copy `example.cfg` to `config.cfg`
* [create new Github app](https://github.com/settings/applications/new) for Oauth with github. set its callback URL to `http://127.0.0.1:5000/callback`
* back to the `config.cfg` file you copied under `tweeza/instance`, past you Github consumer key and consumer secret there, edit your email config and whatever fits you better (caching ..etc).
* restart the app to read the new `condig.cfg` file

That's it! to exit the virtual Python environment, type:`deactivate`.

# Technical information

* Obviously, the project relies on Python, actually it's a Python2 project, however the code is forward-compatible with python3 for easier future migration.
* We use [Flask](http://flask.pocoo.org/), a micro -but scalable- framework for Python based on Werkzeug, Jinja 2, extensively documented, very Pythonic and has no design obligations with easier learning curve.
* [MongoDB](http://www.mongodb.org) a schema-less, document-oriented NoSQL database.
* GridFs to store uploaded files instead of filesystem storage.
* [MongoEngine](http://mongoengine.org/), an ORM-like for MongoDB.
* [Bcrypt](http://en.wikipedia.org/wiki/Bcrypt) for password hashing.
* SASS and Compass for CSS styling, we're using Foundation Zurb at  the moment.
* Bower for grabbing and managing Javascript libraries.
* Optionally, [Redis](http://redis.io/) for caching.

# The project structure

```bash
.
├── api # the API part (not yet developed)
│   └── tests # tests for the APIs
├── docs # where the documentation reside
├── tweeza # The Tweeza part 
│   ├── app.py # the main entry file
│   ├── babel.cfg
│   ├── config.py # where all the config goes.
│   ├── extensions.py # Initialization of the extensions we use on the project
│   ├── frontend   # where everything public    --|
│   ├── dashboard  # the administrative part    --|\ these are the blueprints
│   ├── items      # the items logic and models --|/ (the main parts of the
│   ├── users      # User Auth and profiles     --|         tweeza app)
│   ├── messages.pot # the localization strings goes here.
│   ├── static # everything static (js/css/images..)
│   │   ├── bower.json
│   │   ├── images
│   │   ├── css
│   │   ├── js
│   │   ├── scss # where the SASS files reside
│   │   └── vendors # third-party js libraries, like jQuery, Modernizr... etc
│   ├── templates # HTML templates
│   ├── tests # the test suite for Tweeza
│   ├── translations # generated and compiled translations
│   ├── utils.py # useful functions and/or classes goes here
│   └── manage.py # some useful automated scripts for the app
.
```

### Versioning 

`<major>`.`<minor>`.`<fix>`


# Testing

Unit tests are under development.

# How to contribute

Soon. but if you really want to, be sure to write a [PEP](http://www.python.org/dev/peps/pep-0008)-compatible Python code :)

# TODO

- ☐ Automate the frontend development with Grunt.
- ☐ The APIs part (I'm considering the use of [python-eve](http://python-eve.org/), please tell me if you have a better suggestion on how to design the APIs).
- ☐ Docs/Wiki (coming soon).


# License

Before reading this, please keep in mind that this license doesn't affect the items uploaded on the host server(s), those items have their own licenses.

The source code of this web application and its APIs are under MPL (Mozilla Public License) version 2. See the LICENSE file.

In short you have the right to:

* Copy, Distribute, Modify, as long as you're giving the source code under the same license.
* Private use (e.g. using this web app inside your company or organization for managing its reusable items there) without revealing the source of your custom code you've added. You can as well make profit of it.
* Any public distribution (like another website other than dzlibs.io) has to give the added source code.