# Import Dependencies
import sqlalchemy
import sqlite3
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func
import os
from flask import Flask, jsonify



path ="C:\\Users\\kelly\\OneDrive\\Desktop\\sqlalchemy-challenge"
os.chdir(path)
cwd = os.getcwd()
#print(f"current working directory is {cwd}.")
 #print(new_cwd)
#database setup
# Create our session (link) from Python to the DB
engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo = False)
session = Session(engine)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
#station,date,prcp,tobs
Station = Base.classes.station
#station,name,latitude,longitude,elevation

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)




# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    return (
        f'Welcome to the Vacation Planner API!<br/><br/><br/>'
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

# 4. convert query of precipitation and dates to a dictionary with date as the key and precip as the value
# @app.route("/api/v1.0/precipitation")
# def precipitation():
#     # Create our session (link) from Python to the DB
#     session = Session(engine)

#     """return a tuple list of the precip measurments and their dates within the last year"""
#     # Query all passengers
#     precip_2016 = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= last_year).all()

#     session.close()

#     # Convert list of tuples into normal dict
#     all_names = dict(np.ravel(precip_2016))

#     return jsonify(all_names)

#query the names of all the stations
@app.route("/api/v1.0/stations")
def stations():
    

    #query all stations within the dataset
    all_stations = session.query(Measurement.station).group_by(Measurement.station).all()

    return jsonify(all_stations)

#

if __name__ == "__main__":
    app.run(debug=True)