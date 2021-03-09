"""
Models for Shopcart Resource

All of the models are stored in this module
"""
import logging
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()

class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """
    pass

DATETIME_FORMAT='%Y-%m-%d %H:%M:%S.%f'

######################################################################
#  P E R S I S T E N T   B A S E   M O D E L
######################################################################
class PersistentBase():
    """ Base class added persistent methods """

    def create(self):
        """
        Creates a Account to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def save(self):
        """
        Updates a Account to the database
        """
        logger.info("Saving %s", self.name)
        db.session.commit()

    def delete(self):
        """ Removes a Account from the data store """
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def init_db(cls, app):
        """ Initializes the database session """
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the records in the database """
        logger.info("Processing all records")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """ Finds a record by it's ID """
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_or_404(cls, by_id):
        """ Find a record by it's id """
        logger.info("Processing lookup or 404 for id %s ...", by_id)
        return cls.query.get_or_404(by_id)


######################################################################
#  I T E M   M O D E L
######################################################################
class Item(db.Model, PersistentBase):
    """
    Class that represents which items (and details about those items) for a given shopcart
    """

    app = None

    # Table Schema
    item_id = db.Column(db.String(64), primary_key=True)
    item_name = db.Column(db.String(64), nullable=False)
    shopcart_id = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False) #not with dollar sign
    quantity = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Not really sure what this function does
    def __repr__(self):
        return "<Item %r id=[%s]> shopcart=[%s]" % (self.item_name, self.item_id, self.shopcart_id)


    def serialize(self):
        """ Serializes Items in a Shopcart into a dictionary """
        item_cart = {
            "item_id": self.item_id,
            "item_name": self.item_name,
            "shopcart_id": self.shopcart_id,
            "price": self.price,
            "quantity": self.quantity
            "date_added": self.date_added.strftime(DATETIME_FORMAT)
        }

    def deserialize(self, data):
        """
        Deserializes Items in a Shopcart from a dictionary
        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.item_id = data["item_id"]
            self.item_name = data["item_name"]
            self.shopcart_id = data["shopcart_id"]
            self.price = data["price"]
            self.quantity = data["quantity"]
            self.date_added = datetime.strptime(data["date_added"], DATETIME_FORMAT)
        except KeyError as error:
            raise DataValidationError("Invalid Item Cart: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid Item Cart: body of request contained" "bad or no data"
            )
        return self

    @classmethod
    def find_by_name(cls, name):
        """ Returns all Items with the given name
        Args:
            name (string): the name of the Accounts you want to match
        """
        logger.info("Processing name query for %s ...", item_name)
        return cls.query.filter(cls.item_name == item_name)



######################################################################
#  S H O P C A R T   M O D E L
######################################################################
class Shopcart(db.Model, PersistentBase):
    """
    Class that represents which customer is associated with a given shopcart
    """

    # Table Schema
    shopcart_id = db.Column(db.Integer, primary_key=True)
    # not sure if the customer_id needs to be a foreign key
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    item_list = db.relationship('Item', backref='shopcart', lazy=True)  

    def __repr__(self):
        return "<Shopcart %r shopcart_id=[%s]>" % (self.name, self.shopcart_id)

    def serialize(self):
        """ Serializes a Shopcart into a dictionary """
        return {
            "shopcart_id": self.shopcart_id,
            "customer_id": self.customer_id,
            "item_list": []
        }
        for item in self.item_list:
            shopcart['item_list'].append(item.serialize())
        return shopcart

    def deserialize(self, data):
        """
        Deserializes a Shopcart from a dictionary
        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            "shopcart_id": data["shopcart_id"],
            "customer_id": data["customer_id"],
            "item_list": data.get("item_list")
            for json_address in item_list:
                item = Item()
                item.deserialize(json_address)
                self.item_list.append(address)
        except KeyError as error:
            raise DataValidationError("Invalid Shopcart: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid Shopcart: body of request contained" "bad or no data"
            )
        return self