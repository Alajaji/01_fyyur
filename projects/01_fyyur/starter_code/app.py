#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from forms import *
from flask_wtf import Form
from logging import Formatter, FileHandler
import logging
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
import json
import dateutil.parser
from flask_migrate import Migrate
import sys
import babel
import datetime
from models import *


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

# list all venues in the venues page
@app.route('/venues')
def venues():
    data = []
    current_time = datetime.datetime.now()
    venues = Venue.query.order_by(Venue.city).all()
    dict = {}
    cities = []

    venues_list = []

    for venue in venues:
        num_shows = 0
        for show in venue.shows:
            if (show.start_time > current_time):
                num_shows += 1
        if venue.city not in cities:
            venues_list = [{
                "id": venue.id,
                "name": venue.name,
                "num_upcoming_shows": num_shows,
            }]
            dict = {
                "city": venue.city,
                "state": venue.state,
                "venues": venues_list
            }
            cities.append(venue.city)
            data.append(dict)
        else:
            new_venue = {
                "id": venue.id,
                "name": venue.name,
                "num_upcoming_shows": num_shows,
            }
            venues_list.append(new_venue)
            data[-1]['venues'] = venues_list
    return render_template('pages/venues.html', areas=data)

# search available venues


@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_term = request.form.get('search_term', '')
    form = "%{}%".format(search_term)
    result = Venue.query.filter(Venue.name.ilike(form)).all()
    response = {
        "count": len(result),
        "data": result
    }

    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

# Show venue's information


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    current_time = datetime.datetime.now()
    past_shows = []
    upcoming_shows = []

    venue = Venue.query.filter(Venue.id == venue_id).one()

    past_shows_query = db.session.query(Show).join(
        Venue).filter(Venue.id == venue_id, Show.start_time < current_time).all()

    past_shows_count = len(past_shows_query)

    upcoming_shows_query = db.session.query(Show).join(
        Venue).filter(Venue.id == venue_id, Show.start_time > current_time).all()

    upcoming_shows_count = len(upcoming_shows_query)

    for show in past_shows_query:
        past_shows.append({
            "artist_id": show.artist_id,
            "artist_name": show.Artist.name,
            "artist_image_link": show.Artist.image_link,
            "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
        })

    for show in upcoming_shows_query:
        upcoming_shows.append({
            "artist_id": show.artist_id,
            "artist_name": show.Artist.name,
            "artist_image_link": show.Artist.image_link,
            "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
        })

    print("============")
    print("============")
    data = {
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "image_link": venue.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": past_shows_count,
        "upcoming_shows_count": upcoming_shows_count,
    }

    '''
    data = []
    current_time = datetime.datetime.now()
    venues = Venue.query.order_by(Venue.city).all()
    dict = {}
    for venue in venues:
        past_shows_count = 0
        upcoming_shows_count = 0
        past_shows = []
        upcoming_shows = []
        for show in venue.shows:
            if (show.start_time > current_time):
                upcoming_shows.append({
                    "artist_id": show.artist_id,
                    "artist_name": show.Artist.name,
                    "artist_image_link": show.Artist.image_link,
                    "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
                })
                upcoming_shows_count += 1
            else:
                past_shows.append({
                    "artist_id": show.artist_id,
                    "artist_name": show.Artist.name,
                    "artist_image_link": show.Artist.image_link,
                    "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
                })
                past_shows_count += 1
        dict = {
            "id": venue.id,
            "name": venue.name,
            "genres": venue.genres,
            "address": venue.address,
            "city": venue.city,
            "state": venue.state,
            "phone": venue.phone,
            "website": venue.website,
            "facebook_link": venue.facebook_link,
            "seeking_talent": venue.seeking_talent,
            "image_link": venue.image_link,
            "past_shows": past_shows,
            "upcoming_shows": upcoming_shows,
            "past_shows_count": past_shows_count,
            "upcoming_shows_count": upcoming_shows_count,
        }
        data.append(dict)

    data = list(filter(lambda d: d['id'] ==
                       venue_id, data))[0]
                       '''
    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------


@ app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@ app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # TODOne: insert form data as a new Venue record in the db, instead
    # TODOne: modify data to be the data object returned from db insertion
    error = False
    form = VenueForm()

    try:
        name = request.form.get('name')
        city = request.form.get('city')
        state = request.form.get('state')
        genres = request.form.get('genres')
        phone = request.form.get('phone')
        address = request.form.get('address')
        seeking_talent = request.form.get('seeking_talent')
        seeking_description = request.form.get('seeking_description')
        website = request.form.get('website')
        facebook_link = request.form.get('facebook_link')
        image_link = request.form.get('image_link')

        venue = Venue(name=name, city=city, state=state, genres=genres, phone=phone, address=address,
                      seeking_talent=seeking_talent, seeking_description=seeking_description, website=website, facebook_link=facebook_link, image_link=image_link)
        db.session.add(venue)
        db.session.commit()
    except:
        error = True
        flash('An error occurred. Venue ' +
              request.form.get('name') + ' could not be listed.')
        db.session.rollback()
        print("=========================")
        print(sys.exc_info())
        print("=========================")
    finally:
        db.session.close()
    if not error:
        flash('Venue ' + request.form.get('name') + ' was successfully listed!')

    # on successful db insert, flash success
    # TODOne: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@ app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODOne: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    try:
        Venue.query.filter(Venue.id == venue_id).delete()
        db.session.commit()
    except:
        error = True
        flash('An error occurred. Venue ' +
              request.form.get('name') + ' could not be deleted.')
        db.session.rollback()
        print("=========================")
        print(sys.exc_info())
        print("=========================")
    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return None

#  Artists
#  ----------------------------------------------------------------


@ app.route('/artists')
def artists():
    # TODONE: replace with real data returned from querying the database

    artists = Artist.query.all()
    data = []
    for artist in artists:
        dict = {
            "id": artist.id,
            "name": artist.name,
        }
        data.append(dict)
        '''
    data = [{
        "id": 4,
        "name": "Guns N Petals",
    }, {
        "id": 5,
        "name": "Matt Quevedo",
    }, {
        "id": 6,
        "name": "The Wild Sax Band",
    }]
    '''
    return render_template('pages/artists.html', artists=data)


@ app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODONE: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    '''
    response = {
        "count": 1,
        "data": [{
            "id": 4,
            "name": "Guns N Petals",
            "num_upcoming_shows": 0,
        }]
    }'''

    search_term = request.form.get('search_term', '')
    form = "%{}%".format(search_term)
    result = Artist.query.filter(Artist.name.ilike(form)).all()
    response = {
        "count": len(result),
        "data": result
    }
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@ app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    # TODONE: replace with real venue data from the venues table, using venue_id
    '''
    data1 = {
        "id": 4,
        "name": "Guns N Petals",
        "genres": ["Rock n Roll"],
        "city": "San Francisco",
        "state": "CA",
        "phone": "326-123-5000",
        "website": "https://www.gunsnpetalsband.com",
        "facebook_link": "https://www.facebook.com/GunsNPetals",
        "seeking_venue": True,
        "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
        "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
        "past_shows": [{
            "venue_id": 1,
            "venue_name": "The Musical Hop",
            "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
            "start_time": "2019-05-21T21:30:00.000Z"
        }],
        "upcoming_shows": [],
        "past_shows_count": 1,
        "upcoming_shows_count": 0,
    }
    data2 = {
        "id": 5,
        "name": "Matt Quevedo",
        "genres": ["Jazz"],
        "city": "New York",
        "state": "NY",
        "phone": "300-400-5000",
        "facebook_link": "https://www.facebook.com/mattquevedo923251523",
        "seeking_venue": False,
        "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
        "past_shows": [{
            "venue_id": 3,
            "venue_name": "Park Square Live Music & Coffee",
            "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
            "start_time": "2019-06-15T23:00:00.000Z"
        }],
        "upcoming_shows": [],
        "past_shows_count": 1,
        "upcoming_shows_count": 0,
    }
    data3 = {
        "id": 6,
        "name": "The Wild Sax Band",
        "genres": ["Jazz", "Classical"],
        "city": "San Francisco",
        "state": "CA",
        "phone": "432-325-5432",
        "seeking_venue": False,
        "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "past_shows": [],
        "upcoming_shows": [{
            "venue_id": 3,
            "venue_name": "Park Square Live Music & Coffee",
            "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
            "start_time": "2035-04-01T20:00:00.000Z"
        }, {
            "venue_id": 3,
            "venue_name": "Park Square Live Music & Coffee",
            "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
            "start_time": "2035-04-08T20:00:00.000Z"
        }, {
            "venue_id": 3,
            "venue_name": "Park Square Live Music & Coffee",
            "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
            "start_time": "2035-04-15T20:00:00.000Z"
        }],
        "past_shows_count": 0,
        "upcoming_shows_count": 3,
    }

    data = []
    current_time = datetime.datetime.now()
    artists = Artist.query.all()
    dict = {}
    for artist in artists:
        past_shows_count = 0
        upcoming_shows_count = 0
        past_shows = []
        upcoming_shows = []
        for show in artist.shows:
            if (show.start_time > current_time):
                upcoming_shows.append({
                    "venue_id": show.venue_id,
                    "venue_name": show.Venue.name,
                    "venue_image_link": show.Venue.image_link,
                    "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
                })
                upcoming_shows_count += 1
            else:
                past_shows.append({
                    "venue_id": show.venue_id,
                    "venue_name": show.Venue.name,
                    "venue_image_link": show.Venue.image_link,
                    "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
                })
                past_shows_count += 1
        dict = {
            "id": artist.id,
            "name": artist.name,
            "genres": artist.genres,
            "city": artist.city,
            "state": artist.state,
            "phone": artist.phone,
            "website": artist.website,
            "facebook_link": artist.facebook_link,
            "seeking_venue": artist.seeking_venue,
            "seeking_description": artist.seeking_description,
            "image_link": artist.image_link,
            "past_shows": past_shows,
            "upcoming_shows": upcoming_shows,
            "past_shows_count": past_shows_count,
            "upcoming_shows_count": upcoming_shows_count,
        }
        print('===============================================')
        print(artist.genres)
        print('===============================================')
        data.append(dict)

    data = list(filter(lambda d: d['id'] ==
                       artist_id, data))[0]
    return render_template('pages/show_artist.html', artist=data)
    '''

    current_time = datetime.datetime.now()
    past_shows = []
    upcoming_shows = []

    artist = Artist.query.filter(Artist.id == artist_id).one()

    past_shows_query = db.session.query(Show).join(
        Artist).filter(Artist.id == artist_id, Show.start_time < current_time).all()

    past_shows_count = len(past_shows_query)

    upcoming_shows_query = db.session.query(Show).join(
        Artist).filter(Artist.id == artist_id, Show.start_time > current_time).all()

    upcoming_shows_count = len(upcoming_shows_query)

    for show in past_shows_query:
        past_shows.append({
            "venue_id": show.venue_id,
            "venue_name": show.Venue.name,
            "venue_image_link": show.Venue.image_link,
            "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
        })

    for show in upcoming_shows_query:
        upcoming_shows.append({
            "venue_id": show.venue_id,
            "venue_name": show.Venue.name,
            "venue_image_link": show.Venue.image_link,
            "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
        })

    data = {
        "id": artist.id,
        "name": artist.name,
        "genres": artist.genres,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": past_shows_count,
        "upcoming_shows_count": upcoming_shows_count,
    }
    return render_template('pages/show_artist.html', artist=data)
#  Update
#  ----------------------------------------------------------------


@ app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):

    artist = Artist.query.filter(Artist.id == artist_id).one()
    form = ArtistForm(name=artist.name,
                      city=artist.city,
                      state=artist.state,
                      genres=artist.genres,
                      phone=artist.phone,
                      seeking_venue=artist.seeking_venue,
                      seeking_description=artist.seeking_description,
                      website=artist.website,
                      facebook_link=artist.facebook_link,
                      image_link=artist.image_link)
    '''
    form = ArtistForm()
    artist = {
        "id": form,
        "name": "Guns N Petals",
        "genres": ["Rock n Roll"],
        "city": "San Francisco",
        "state": "CA",
        "phone": "326-123-5000",
        "website": "https://www.gunsnpetalsband.com",
        "facebook_link": "https://www.facebook.com/GunsNPetals",
        "seeking_venue": True,
        "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
        "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
    }
    '''
    # TODOne: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@ app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODOne: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    error = False

    try:
        name = request.form.get('name')
        city = request.form.get('city')
        state = request.form.get('state')
        genres = request.form.get('genres')
        phone = request.form.get('phone')
        seeking_venue = request.form.get('seeking_venue')
        seeking_description = request.form.get('seeking_description')
        website = request.form.get('website')
        facebook_link = request.form.get('facebook_link')
        image_link = request.form.get('image_link')

        artist = {"name": name, "city": city, "state": state, "genres": genres, "phone": phone, "seeking_venue": seeking_venue,
                  "website": website, "facebook_link": facebook_link, "image_link": image_link}
        Artist.query.filter(Artist.id == artist_id).update(artist)
        db.session.commit()
    except:
        error = True
        flash('An error occurred. Artist ' +
              request.form.get('name') + ' could not be updated.')
        db.session.rollback()
        print("=========================")
        print(sys.exc_info())
        print("=========================")
    finally:
        db.session.close()
    if not error:
        flash('Artist ' + request.form.get('name') +
              ' was successfully updated!')
    return redirect(url_for('show_artist', artist_id=artist_id))


@ app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    venue = Venue.query.filter(Venue.id == venue_id).one()
    form = VenueForm(name=venue.name,
                     city=venue.city,
                     state=venue.state,
                     genres=venue.genres,
                     phone=venue.phone,
                     address=venue.address,
                     seeking_talent=venue.seeking_talent,
                     seeking_description=venue.seeking_description,
                     website=venue.website,
                     facebook_link=venue.facebook_link,
                     image_link=venue.image_link)

    '''
    venue = {
        "id": 1,
        "name": "The Musical Hop",
        "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
        "address": "1015 Folsom Street",
        "city": "San Francisco",
        "state": "CA",
        "phone": "123-123-1234",
        "website": "https://www.themusicalhop.com",
        "facebook_link": "https://www.facebook.com/TheMusicalHop",
        "seeking_talent": True,
        "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
        "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
    }'''
    # TODOne: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@ app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODOne: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    error = False

    try:
        name = request.form.get('name')
        city = request.form.get('city')
        state = request.form.get('state')
        genres = request.form.get('genres')
        phone = request.form.get('phone')
        address = request.form.get('address')
        seeking_talent = request.form.get('seeking_talent')
        seeking_description = request.form.get('seeking_description')
        website = request.form.get('website')
        facebook_link = request.form.get('facebook_link')
        image_link = request.form.get('image_link')

        venue = {"name": name, "city": city, "state": state, "genres": genres, "phone": phone, "address": address, "seeking_talent": seeking_talent,
                 "website": website, "facebook_link": facebook_link, "image_link": image_link}
        Venue.query.filter(Venue.id == venue_id).update(venue)
        db.session.commit()
    except:
        error = True
        flash('An error occurred. Venue ' +
              request.form.get('name') + ' could not be updated.')
        db.session.rollback()
        print("=========================")
        print(sys.exc_info())
        print("=========================")
    finally:
        db.session.close()
    if not error:
        flash('Venue ' + request.form.get('name') + ' was successfully updated!')

    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@ app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@ app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODOne: insert form data as a new Venue record in the db, instead
    # TODOne: modify data to be the data object returned from db insertion

    error = False
    form = ArtistForm()

    try:
        name = request.form.get('name')
        city = request.form.get('city')
        state = request.form.get('state')
        genres = request.form.get('genres')
        phone = request.form.get('phone')
        seeking_venue = request.form.get('seeking_venue')
        seeking_description = request.form.get('seeking_description')
        website = request.form.get('website')
        facebook_link = request.form.get('facebook_link')
        image_link = request.form.get('image_link')

        artist = Artist(name=name, city=city, state=state, genres=genres, phone=phone,
                        seeking_venue=seeking_venue, seeking_description=seeking_description, website=website, facebook_link=facebook_link, image_link=image_link)
        db.session.add(artist)
        db.session.commit()
    except:
        error = True
        flash('An error occurred. Artist ' +
              request.form.get('name') + ' could not be listed.')
        db.session.rollback()
        print("=========================")
        print(sys.exc_info())
        print("=========================")
    finally:
        db.session.close()
    if not error:
        flash('Artist ' + request.form.get('name') + ' was successfully listed!')
    # on successful db insert   , flash success
    # flash('Artist ' + request.form['name'] + ' was successfully listed!')
    # TODOne: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@ app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODONE: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    '''
    data = [{
        "venue_id": 1,
        "venue_name": "The Musical Hop",
        "artist_id": 4,
        "artist_name": "Guns N Petals",
        "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
        "start_time": "2019-05-21T21:30:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 5,
        "artist_name": "Matt Quevedo",
        "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
        "start_time": "2019-06-15T23:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-01T20:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-08T20:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-15T20:00:00.000Z"
    }]'''

    data = []
    dict = {}
    shows = Show.query.all()
    for show in shows:
        dict = {
            "venue_id": show.Venue.id,
            "venue_name": show.Venue.name,
            "artist_id": show.Artist.id,
            "artist_name": show.Artist.name,
            "artist_image_link": show.Artist.image_link,
            "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
        }
        data.append(dict)

    return render_template('pages/shows.html', shows=data)


@ app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@ app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODOne: insert form data as a new Show record in the db, instead
    error = False
    form = ShowForm()

    try:
        artist_id = request.form.get('artist_id')
        venue_id = request.form.get('venue_id')
        start_time = request.form.get('start_time')

        show = Show(artist_id=artist_id, venue_id=venue_id,
                    start_time=start_time)
        db.session.add(show)
        db.session.commit()
    except:
        error = True
        flash('An error occurred. Show could not be listed.')
        db.session.rollback()
        print("=========================")
        print(sys.exc_info())
        print("=========================")
    finally:
        db.session.close()
    if not error:
        flash('Show was successfully listed!')
    # on successful db insert, flash success
    # flash('Show was successfully listed!')
    # TODOne: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@ app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@ app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
