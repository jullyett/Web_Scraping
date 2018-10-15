# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# create route that renders index.html template and finds documents from mongo
@app.route("/")
def home():

    # Find data
    Mars = mongo.db.info.find()

    # return template and data
    return render_template("index.html", scraped_data = Mars)


# Route that will trigger scrape functions
@app.route("/scrape")
def scrape(): 

    info = mongo.db.info

    # Run scraped functions
    mars_dict = scrape_mars.scrape()

    # Store results into a dictionary
    mars_data = {
        "headline": mars_dict["latest_headline"],
        "text": mars_dict["latest_text"],
        "featured_image": mars_dict["featured_image"],
        "Weather_mars": mars_dict["Mars_weather"],
        "facts_table": mars_dict["Mars_table"],
        "hemispheres": mars_dict["Hemispheres"]
    }

    # Insert dictionary into database
    mongo.db.info.drop()
    mongo.db.info.insert_one(mars_data)

    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
