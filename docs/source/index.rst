Flask-Webhelpers
*************

.. module:: flask_webhelpers

The **Flask-Webhelpers** extension helps integrate Webhelpers in your Flask web applications.

Installing Flask-Webhelpers
========================

Install with **pip** and **easy_install**::

    pip install Flask-Webhelpers

or download the latest version from version control::

    git clone https://github.com/bngsudheer/Flask-Webhelpers.git
    cd flask-webhelpers
    python setup.py develop

If you are using **virtualenv**, it is assumed that you are installing **Flask-Webhelpers**
in the same virtualenv as your Flask application(s).

Using Flask-Webhelpers
=============
Import the ObjectGrid component of Flask-Webhelpers::

    from flask.ext.webhelpers import ObjectGrid

    grid = ObjectGrid(
        request=request,
        itemlist=users,
        columns=['username', 'full_name', 'action']
    )

In this example, users is a collection of users. It can be the SQLAlchemy ResultProxy or a list of user objects. We also pass along the request object to the grid. The columns argument takes a list of allowed columns to be rendered in the grid. 'action' column does not exist in our user object. We add it as an extra column in the grid. 

In your template, you could simply render the grid::
    {{ grid|safe }}

Now we have the basic grid.

Customizing the column output
============
Perhaps, you want to add some links or buttons in the 'action' column. You can assign a function to handle the output of the column. When the column is being rendered in the grid, your function will be called:: 

    def action_markup(column_number, i, item):
        return my_action_code

Like the name suggests 'column_number' is the column's number in the row. 'item' is the current item in users' iteration.

If you are including HTML markup in the customization function, wrap in the 'literal'::

    from webhelpers.html.builder import literal

    def action_markup(column_number, i, item):
        return literal(my_action_code)

The function is assigned for columns by setting a dict to grid.column_formats::
      grid.column_formats = {
        'action': action_markup,
      }


Generating ordering links in the header columns
==========
Flask-Webhelperss makes it easy to setup ordering links for the grid header columns. The column names can be wrapped in an anchor tag like::
    <a href="/current/path?order_col=username&amp;order_dir=asc">Username</a>

Exclude the list of columns for which ordering links are not required::
    grid.exclude_ordering = ['action']



