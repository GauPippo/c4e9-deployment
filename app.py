"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""

import os
import mlab
from mongoengine import *
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')

app.config["IMG_PATH"] = os.path.join(app.root_path,"static", 'img')
# print(app.root_path)
# print(os.path.join(app.root_path, "static"))

    # 1.Connect mlab:
mlab.connect()

    # 2. Create data in db:
# item1 = Item(image="https://s-media-cache-ak0.pinimg.com/originals/06/08/22/060822f637a48eee7a376fe2813e42d9.jpg",
#             title = "Bagwell",
#             price = 5000)
# item1.save()

class Item(Document):
    image = StringField()
    title = StringField()
    price = FloatField()

@app.route('/') #Home page
def index():
    return render_template("index.html", items = Item.objects())

@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')

@app.route('/images/<image_name>')
def image(image_name):
    return send_from_directory(app.config["IMG_PATH"],image_name)

@app.route('/add-lingerie', methods=["GET","POST"])
def add_lingerie():
    #Client asking for FORM
    if request.method == "GET":
        return render_template("add_item.html")

    #Client submiting FORM
    elif request.method == "POST":
        #1.Get data from FORM: title, image, price
        #Validate input

        form = request.form
        title = form["title"]
        # image = form["image"]
        price = form["price"]

        image = request.files["image"]
        filename = secure_filename(image.filename) # make image name machine-friendly.
        save_location = os.path.join(app.config["IMG_PATH"], filename)
        image.save(save_location)

        #2. Create data(database)
        item = Item(title = title,
                    image = "images/{0}".format(filename),
                    price = price)
        item.save()

        # #3. Redirect

        return redirect(url_for("index"))

###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=False)
