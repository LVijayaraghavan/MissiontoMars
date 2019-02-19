from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():


    # Find one record of data from the mongo database
    # @TODO: YOUR CODE HERE!

    # Return template and data
    mars_data = mongo.db.mars_info.find_one()
    return render_template("index.html", Mars_data=mars_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function and save the results to a variable
    # @TODO: YOUR CODE HERE!

    mars_collection = mongo.db.mars_info
    mars_info = scrape_mars.scrape()
    mars_collection.update({}, mars_info, upsert=True)
    return redirect("/", code=302)

    # Update the Mongo database using update and upsert=True
    # @TODO: YOUR CODE HERE!

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
