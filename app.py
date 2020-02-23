# Import Dependencies
import sqlalchemy
import sqlite3
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func
import os
from flask import Flask, jsonify, g


#change working directory to correct directory
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
        f"/api/v1.0/'startdateyyyy-mm-dd'<br/>"
        f"/api/v1.0/'startdateyy-mm-dd'/'enddateyy-mm-dd'<br/>"
    )

# 4. convert query of precipitation and dates to a dictionary with date as the key and precip as the value
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #return a tuple list of the precip measurments and their dates within the last year
    # Query all precipitation measurements
    last_year = '2016-08-23'
    precip_2016 = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= last_year).all()
    precip_dict=dict((x, y) for x, y in precip_2016)
    return jsonify(precip_dict)
     
    #session.close()



#query the names of all the stations
@app.route("/api/v1.0/stations")
def stations():
    

    #query all stations within the dataset
    all_stations = session.query(Measurement.station).group_by(Measurement.station).all()

    return jsonify(all_stations)

# #
#query the dates and temperatures a year from the last observation
@app.route("/api/v1.0/tobs")
def tobs():
    

    #query all stations within the dataset
    last_year = '2016-08-23'
    year_of_tobs = session.query(Measurement.tobs).filter(Measurement.date >= last_year).all()

    return jsonify(year_of_tobs)

#
@app.route("/api/v1.0/<start_date>")
def temps(start_date):
    # TMIN, TAVG, and TMAX for a list of dates.
    
    # Args:
    #     start_date (string): A date string in the format %Y-%m-%d
    #     end_date (string): A date string in the format %Y-%m-%d
        
    # Returns:
    #     TMIN, TAVE, and TMAX

    searched_temps =session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    
 
    canonicalized = start_date.replace("/", "-")
    for date in Measurement.date:
        search_date = date['start_date'].replace("/", "-")

        if start_date == canonicalized:
            return jsonify(searched_temps)
    else:
        return jsonify({'error:'f"{start_date} not found."}), 404
        

    
 


@app.route("/api/v1.0/<start_date>/<end_date>")
def calc_temps(start_date, end_date):
    #TMIN, TAVG, and TMAX for a list of dates.
    
    # Args:
    #     start_date (string): A date string in the format %Y-%m-%d
    #     end_date (string): A date string in the format %Y-%m-%d
        
    # Returns:
    #     TMIN, TAVE, and TMAX
    
    
    start_and_end= session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    canonicalized1 = start_date.replace("/", "-")

    canonicalized2 = end_date.replace("/", "-")

    if start_date == canonicalized1 and end_date == canonicalized2:
        return jsonify(start_and_end)
    else:
        return jsonify({'error:'f"{start_date, end_date} not found."}), 404

if __name__ == "__main__":
    app.run(debug=True)