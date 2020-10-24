
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from logging import Formatter, FileHandler
import logging
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask import Flask, render_template, request, Response, flash, redirect, url_for
import json
import dateutil.parser
from flask_migrate import Migrate
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)))
    phone = db.Column(db.String(120))
    address = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String)
    website = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    shows = db.relationship('Show', backref='Venue')

    def __repr__(self):
        return str(self.__dict__)
        # return f'<Venue {self.id} {self.name} {self.city} {self.state} {self.address}>'

    # TODONE: implement any missing fields, as a database migration using Flask-Migrate


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String)
    website = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    shows = db.relationship('Show', backref='Artist')

    # TODONE: implement any missing fields, as a database migration using Flask-Migrate

# TODONE Implement Show and Artist models, and complete all model relationships and properties, as a database migration.


class Show(db.Model):
    __tablename__ = 'Show'
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'))
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'))
