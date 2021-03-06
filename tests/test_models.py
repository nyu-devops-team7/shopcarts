# Copyright 2016, 2019 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test cases for Shopcart Model
Test cases can be run with:
    nosetests
    coverage report -m
While debugging just these tests it's convinient to use this:
    nosetests --stop tests/test_models.py:TestShopcart
"""
import logging
import unittest
import os
from service.models import Shopcart, Item, DataValidationError, db
from service import app
from .factories import ShopcartFactory, ItemFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
)

######################################################################
#  S H O P C A R T    M O D E L   T E S T   C A S E S
######################################################################
class TestShopcart(unittest.TestCase):
    """ Test Cases for Shopcart Model """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Shopcart.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        db.session.close()

    def setUp(self):
        """ This runs before each test """
        db.drop_all()  # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()
        db.drop_all()

######################################################################
#  H E L P E R   M E T H O D S
######################################################################

    def _create_shopcart(self, items=[]):
        """ Creates an Shopcart from a Factory """
        fake_shopcart = ShopcartFactory()
        shopcart = Shopcart(
            customer_id=fake_shopcart.customer_id,
            items_list=items
        )
        self.assertTrue(shopcart != None)
        return shopcart

    def _create_item(self):
        """ Creates fake items from factory """
        fake_item = ItemFactory()
        item = Item(
            item_name=fake_item.item_name,
            item_quantity=fake_item.item_quantity,
            item_price=fake_item.item_price,
        )
        self.assertTrue(item != None)
        return item

######################################################################
#  T E S T   C A S E S
######################################################################

    def test_XXXX(self):
        """ Test to make sure stuff is working """
        self.assertTrue(True)

    def test_create_a_shopcart(self):
        """ Create a Shopcart and assert that it exists """
        fake_shopcart = ShopcartFactory()
        shopcart = Shopcart(
            id=fake_shopcart.id, 
            customer_id=fake_shopcart.customer_id, 
        )
        self.assertTrue(shopcart != None)
        self.assertEqual(shopcart.id, fake_shopcart.id)
        self.assertEqual(shopcart.customer_id, fake_shopcart.customer_id)

    def test_create_an_item(self):
        """ Create an Item and assert that it exists """
        fake_item = ItemFactory()
        item = Item(
            id=fake_item.id,
            item_name=fake_item.item_name,
            item_quantity=fake_item.item_quantity,
            item_price=fake_item.item_price
        )
        self.assertTrue(item != None)
        self.assertEqual(item.id, fake_item.id)
        self.assertEqual(item.item_name, fake_item.item_name)
        self.assertEqual(item.item_quantity, fake_item.item_quantity)
        self.assertEqual(item.item_price, fake_item.item_price)


    def test_delete_an_shopcart(self):
        """ Delete an shopcart from the database """
        shopcarts = Shopcart.all()
        self.assertEqual(shopcarts, [])
        shopcart = self._create_shopcart()
        shopcart.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertEqual(shopcart.id, 1)
        shopcarts = Shopcart.all()
        self.assertEqual(len(shopcarts), 1)
        shopcart = shopcarts[0]
        shopcart.delete()
        shopcarts = Shopcart.all()
        self.assertEqual(len(shopcarts), 0)

    def test_delete_shopcart_item(self):
        """ Delete an shopcarts item """
        shopcarts = Shopcart.all()
        self.assertEqual(shopcarts, [])

        item = self._create_item()
        shopcart = self._create_shopcart(items=[item])
        shopcart.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertEqual(shopcart.id, 1)
        shopcarts = Shopcart.all()
        self.assertEqual(len(shopcarts), 1)

        # Fetch it back
        shopcarts = Shopcart.find(shopcart.id)
        item = shopcart.items_list[0]
        item.delete()
        shopcart.save()

        # Fetch it back again
        shopcart = Shopcart.find(shopcart.id)
        self.assertEqual(len(shopcart.items_list), 0)
    
    def test_deserialize_with_key_error(self):
        """ Deserialize an Shopcart with a KeyError """
        shopcart = Shopcart()
        self.assertRaises(DataValidationError, shopcart.deserialize, {})

    def test_deserialize_with_type_error(self):
        """ Deserialize an Shopcart with a TypeError """
        shopcart = Shopcart()
        self.assertRaises(DataValidationError, shopcart.deserialize, [])

    def test_deserialize_item_key_error(self):
        """ Deserialize an item with a KeyError """
        item = Item()
        self.assertRaises(DataValidationError, item.deserialize, {})

    def test_deserialize_item_type_error(self):
        """ Deserialize an item with a TypeError """
        item = Item()
        self.assertRaises(DataValidationError, item.deserialize, [])

    def test_add_item_to_shopcart(self):
        """ Create a shopcart with an item and add it to the database """
        shopcarts = Shopcart.all()
        self.assertEqual(shopcarts, [])
        shopcart = self._create_shopcart()
        item = self._create_item()
        shopcart.items_list.append(item)
        shopcart.create()

        # Assert that it was assigned an id and shows up in the database
        self.assertEqual(shopcart.id, 1)
        shopcarts = Shopcart.all()
        self.assertEqual(len(shopcarts), 1)

        new_shopcart = Shopcart.find(shopcart.id)
        self.assertEqual(shopcart.items_list[0].item_name, item.item_name)

        item2 = self._create_item()
        shopcart.items_list.append(item2)
        shopcart.save()

        new_shopcart = Shopcart.find(shopcart.id)
        self.assertEqual(len(shopcart.items_list), 2)
        self.assertEqual(shopcart.items_list[1].item_name, item2.item_name)

    def test_find_by_customer_id(self):
        """ Find by customer_id """
        shopcart = self._create_shopcart()
        shopcart.create()

        # Fetch it back by name
        same_shopcart = Shopcart.find_by_customer_id(shopcart.customer_id)[0]
        self.assertEqual(same_shopcart.customer_id, shopcart.customer_id)
        self.assertEqual(same_shopcart.id, shopcart.id)

    def test_find_by_item_name(self):
        """ Find by item name """
        shopcarts = Shopcart.all()
        self.assertEqual(shopcarts, [])
        shopcart = self._create_shopcart()
        item = self._create_item()
        shopcart.items_list.append(item)
        shopcart.create()

        # Fetch it back by name
        same_item = Item.find_by_item_name(item.item_name)[0]
        self.assertEqual(same_item.id, item.id)
        self.assertEqual(same_item.item_name, item.item_name)
        self.assertEqual(same_item.item_quantity, item.item_quantity)
        self.assertEqual(same_item.item_price, item.item_price)