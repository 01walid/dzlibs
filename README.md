# [DzLibs](dzlibs.io) Project
=============================

A community-driven Algerian index of reusable assets and libraries. see the [about page](dzlibs.io/about)

# Installation

Before walking through the following steps, please make sure you have [MongoDB](http://www.mongodb.org/) installed on your system.

It's highly recommended to install [Pip](https://pypi.python.org/pypi/pip) then [Virtual env](https://pypi.python.org/pypi/virtualenv) 
first, respectively.

For Pip under Ubuntu, try: `apt-get install python-pip` or search the web in case the name of the package has changed. Make sure that the pip package is for Python2 not Python3.

Once Pip installed, you can install Virtualenv by running:

```shell
$ [sudo] pip install virtualenv
```

Then download the source code, and do the following:

```shell
$ cd path/to/the/downloaded/source
# create a virtual isolated python2 environment
$ virtualenv venv # or it may be called virtualenv-2 or something similar...
# activate the new python environment
$ source venv/bin/activate
# now install the project requirements
$ pip install -r requirements.txt
# after downloading launch the project by running:
$ cd tweeza
$ python manage.py runserver
```

If all goes well, you should see something like this in your Terminal:

```shell
 * Running on http://127.0.0.1:5000/
 * Restarting with reloader
```

Then open the following URL in your browser to test the app: http://127.0.0.1:5000.

Exit by `<CTRL> + <C>`.

Exit the virtual Python environment, type:`deactivate`.

# Technical information

* Obviously, the project relies on Python, actually it's a Python2 project, however the code is forward-compatible with python3 for easier future migration.
* We use [Flask](http://flask.pocoo.org/), a micro -but scalable- framework for Python based on Werkzeug, Jinja 2, extensively documented, very Pythonic and has no design obligations with easier learning curve.
* [MongoDB](http://www.mongodb.org) a schema-less, document-oriented NoSQL database.
* [Bcrypt](http://en.wikipedia.org/wiki/Bcrypt) for password hashing.
* SASS and Compass for CSS styling, we're using Foundation Zurb at  the moment.
* [MongoEngine](http://mongoengine.org/), an ORM-like for MongoDB.
* Bower for grabbing and managing Javascript librairies.

# The project structure

```shell
.
├── ara # the API part (not yet developped)
│   └── tests # tests for the APIs
├── docs # where the documentation reside
├── tweeza # The tweeza part 
│   ├── app.py # the main entry file
│   ├── babel.cfg
│   ├── config.py # where all the config goes.
│   ├── extensions.py # Initialisation of the extensions we use on the project
│   ├── frontend   # where everything public    --|
│   ├── dashboard  # the administrative part    --|\ these are the blurpints
│   ├── items      # the items logic and models --|/ (the main parts of the
│   ├── users      # User Auth and profiles     --|         tweeza app)
│   ├── messages.pot # the localization strings goes here.
│   ├── static # everything static (js/css/images..)
│   │   ├── bower.json
│   │   ├── images
│   │   ├── js
│   │   ├── scss # where the SASS files reside
│   │   └── vendors # third-party js librairies, like jQuery, Modernizr... etc
│   ├── templates # HTML templates
│   ├── tests # the test suite for Tweeza
│   ├── translations # generated and compiled translations
│   ├── uploads # where the uploaded items reside
│   ├── utils.py # useful functions and/or classes goes here
│   ├── manage.py
.   .
.
```

### Versioning 

`<major>`.`<minor>`.`<fix>`


# Testing

Unit tests are under development.

# How to contribute

Soon. but if you really want to, be sure to write a [PEP](http://www.python.org/dev/peps/pep-0008)-compatible Python code :)

# TODO

- ☐ Automate the frontend developpment with Grunt.
- ☐ Ara (the APIs part).
- ☐ Docs/Wiki (comming soon).


# License

Before reading this, please keep in mind that this license doesn't affect the items shared on the host server(s), those items have their own licenses.

The source code of this web application and its APIs are under MPL (Mozilla Public License) version 2. See the LICENSE file.

In short you have the right to:

* Copy, Distribute, Modify, as long as you're giving the source code under the same license.
* Private use (e.g. using this web app inside your company or organization for managing reusable items there) without revealing the source of your custom code you've added.





