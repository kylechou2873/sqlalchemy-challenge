# Import the dependencies.
from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

import datetime as dt


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    """List all available api routes."""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Precipitation Result"""
    qD = dt.date(2017,8,23)-dt.timedelta(days=365)
    prcpQ = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >= qD).all()
    prcpR = []
    for date,prcp in prcpQ:
        prcpD = {}
        prcpD["date"] = date
        prcpD["prcp"] = prcp
        prcpR.append(prcpD)
    return jsonify(prcpR)
@app.route("/api/v1.0/stations")
def stations():
    """Stations Dataset"""
    stationQ = session.query(Station.station,Station.name,Station.latitude,Station.longitude,Station.elevation).all()
    allStation = []
    for station,name,latitude,longitude,elevation in stationQ:
        stationD = {}
        stationD["station"] = station
        stationD["name"] = name
        stationD["latitude"] = latitude
        stationD["longitude"] = longitude
        stationD["elevation"] = elevation
        allStation.append(stationD)
    return jsonify(allStation)
@app.route("/api/v1.0/tobs")
def tobs():
    """Most-active station previous year of temperature data"""
    qD = dt.date(2017,8,23)-dt.timedelta(days=365)
    dataQ = session.query(Measurement.date,Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= qD).all()
    dataR = []
    for date,tobs in dataQ:
        dataD = {}
        dataD["date"] = date
        dataD["tobs"] = tobs
        dataR.append(dataD)
    return jsonify(dataR)
@app.route("/api/v1.0/<start>")
def greaterFromStart(start):
    """Fetch and calculate TMIN, TMAX, TAVG for all dates greater than start date(YYYY-MM-DD)"""
    calQ = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).order_by(Measurement.date).filter(Measurement.date >= start).all()
    result = {}
    result["Min Temp"] = calQ[0][0]
    result["Max Temp"] = calQ[0][1]
    result["Avg Temp"] = calQ[0][2]
    return jsonify(result)
@app.route("/api/v1.0/<start>/<end>")
def greaterBtwStEnd(start,end):
    """Fetch and calculate TMIN, TMAX, TAVG for all dates between start date(YYYY-MM-DD) and end date(YYYY-MM-DD)"""
    calQ = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).order_by(Measurement.date).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    result = {}
    result["Min Temp"] = calQ[0][0]
    result["Max Temp"] = calQ[0][1]
    result["Avg Temp"] = calQ[0][2]
    return jsonify(result)

session.close()

if __name__ == '__main__':
    app.run(debug=True)