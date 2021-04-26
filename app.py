from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scraping
from pprint import pprint

app = Flask(__name__)
# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars_record = mongo.db.mars.find_one()
    # pprint(mars_record)
    return render_template("index.html", mars=mars_record)

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scraping.scrape_all()
    # print(mars_data)
    # mars.replace_one({}, mars_data, upsert=True)
    # Redirect back to home page
    mars.update({}, mars_data, upsert=True)
    return redirect("/",code=302)

if __name__ == "__main__":
    app.run()
