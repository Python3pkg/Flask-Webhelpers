# -*- coding: utf-8 -*-
"""
tests/tests.py
======================
This is a testing file for Flask-Webhelpers.

:copyright: 2015 Sudheer Satyanarayana
:license:   BSD, see LICENSE for details
"""


import os
import flask
import unittest

from flask_webhelpers import ObjectGrid


class MyClass(object):
    pass


class TestFlasktWebelpers(unittest.TestCase):

    def get_users(self):
        my_list = []
        for i in range(100):
            my_obj = MyClass()
            my_obj.user_id = i
            my_obj.username = 'username_%s' % i
            my_list.append(my_obj)
        return my_list

    def setUp(self):
        app = flask.Flask(__name__)
        from flask import request
        app.config['TESTING'] = True

        @app.route("/")
        def first():

            my_list = self.get_users()
            grid = ObjectGrid(
                request=request,
                itemlist=my_list,
                columns=['user_id', 'username']
            )

            rendered_grid = str(grid)

            return rendered_grid
        self.app = app

        @app.route("/second")
        def second():
            my_list = self.get_users()

            grid = ObjectGrid(
                request=request,
                itemlist=my_list,
                columns=['user_id', 'username']
            )

            rendered_grid = str(grid)

            return rendered_grid

        @app.route("/third/<int:my_custom_arg>")
        def third(my_custom_arg):
            my_list = self.get_users()

            grid = ObjectGrid(
                request=request,
                itemlist=my_list,
                columns=['user_id', 'username']
            )

            grid.exclude_ordering = []
            rendered_grid = str(grid)

            return rendered_grid

        @app.route("/fourth")
        def fourth():
            my_list = self.get_users()

            grid = ObjectGrid(
                request=request,
                itemlist=my_list,
                columns=['user_id', 'username']
            )

            grid.exclude_ordering = []
            rendered_grid = str(grid)

            return rendered_grid

        @app.route("/fifth")
        def fifth():
            my_list = self.get_users()

            grid = ObjectGrid(
                request=request,
                itemlist=my_list,
                columns=['user_id', 'username', 'action']
            )

            grid.column_formats = {
                'action': lambda column_number, i, item:
                    '<td>Custom Content</td>'
            }

            grid.exclude_ordering = ['action']
            rendered_grid = str(grid)

            return rendered_grid

        @app.route("/sixth")
        def sixth():
            my_list = self.get_users()

            grid = ObjectGrid(
                request=request,
                itemlist=my_list,
                columns=['user_id', 'username']
            )

            grid.exclude_ordering = []
            rendered_grid = str(grid)

            return rendered_grid

        @app.route("/seventh/<int:some_id>")
        def seventh(some_id):
            my_list = self.get_users()

            grid = ObjectGrid(
                request=request,
                itemlist=my_list,
                columns=['user_id', 'username']
            )

            grid.exclude_ordering = []
            rendered_grid = str(grid)

            return rendered_grid

        self.app = app

    def test_basic(self):

        client = self.app.test_client()
        rv = client.get('/')

        assert ('<tr class="odd r1"><td class="c1">0</td><td class="c2">'
                'username_0</td></tr>') in rv.data

    def test_header_th(self):
        client = self.app.test_client()
        rv = client.get('/second')

        assert ('<tr class="header"><th class="c1 user_id">'
                'User Id</th>') in rv.data

    def test_header_view_args(self):
        client = self.app.test_client()
        rv = client.get('/third/10')
        assert ('<th class="c1 ordering user_id">'
                '<a href="/third/10?order_col=user_id&amp;order_dir=asc">'
                'User Id</a>'
                '<span class="marker"></span></th>') in rv.data

    def test_header_request_args(self):
        client = self.app.test_client()
        rv = client.get('/fourth?my_custom_arg=23')
        assert ('<th class="c1 ordering user_id">'
                '<a href="/fourth?order_col=user_id&amp;my_custom_arg=23&amp;'
                'order_dir=asc">User Id</a>'
                '<span class="marker"></span></th>') in rv.data

    def test_custom_col(self):
        client = self.app.test_client()
        rv = client.get('/fifth')
        assert '<th class="c3 action">Action</th>' in rv.data

    def test_header_link(self):
        client = self.app.test_client()
        rv = client.get('/sixth')
        assert ('<th class="c1 ordering user_id">'
                '<a href="/sixth?order_col=user_id&amp;order_dir=asc">'
                'User Id</a>'
                '<span class="marker"></span></th>') in rv.data

    def test_view_args_request_args_combined(self):
        client = self.app.test_client()
        rv = client.get('/seventh/100?some_param=some_value')
        assert ('<a href="/seventh/100?order_col=user_id'
                '&amp;some_param=some_value&amp;order_dir=asc">') in rv.data


if __name__ == '__main__':
    unittest.main()
