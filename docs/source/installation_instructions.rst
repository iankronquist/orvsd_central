====
Setting up ORVSD Central
====
Pre-requisites:
----
In order to setup ORVSD_Central a Database Server is needed with a database called 'central'

Instructions
----
We recommend setting up orvsd_central in a virtualenv.

\1. After sourcing your virtualenv go to your directory which contains 
orvsd_central and run::
    
    pip install -r requirements.txt

\2. Run the following command twice::
    
    python manage.py initdb

**Warning** It won't work the first time. This command has to be run twice.

A prompt for an admin account creation will show, choose any
username, email, and password you wish.

\3. Import district and school data::

    python manage.py import_data -d /path/to/someData.csv 
    
.. This instruction isn't complete until we find a way so the user doesn't need
    download the .csv file.

\4. Gather sitedetail data from existing moodle sites::
    
    python manage.py gather

\5. To run the server::

    python manage.py runserver

There you have it! Test your orvsd_central instance out by going to http://127.0.0.1:5000 in your browser.

