from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime

app = Flask(__name__)

# MongoDB Atlas connection
app.config["MONGO_URI"] = "mongodb+srv://yw4810:RpVFfm25KqQzFtUd@cluster0.z5bytfr.mongodb.net/reviews?retryWrites=true&w=majority&appName=Cluster0"
mongo = PyMongo(app)

# Select the database
db = mongo.db

@app.route('/')
def index():
    reviews = db.all_reviews.find()
    return render_template('index.html', reviews=reviews)

@app.route('/create', methods=['GET'])
def create():
    return render_template('create.html')

@app.route('/create', methods=['POST'])
def create_post():
    db.all_reviews.insert_one({
        'name': request.form['name'],
        'title': request.form['title'],
        'review': request.form['review'],
        'created_at': datetime.now()
    })
    return redirect(url_for('index'))

@app.route('/reviews')
def reviews():
    all_reviews = db.all_reviews.find()
    return render_template('read.html', reviews=all_reviews)

@app.route('/edit/<mongoid>', methods=['GET'])
def edit(mongoid):
    review = db.all_reviews.find_one({'_id': ObjectId(mongoid)})
    return render_template('edit.html', doc=review, mongoid=mongoid)

@app.route('/edit/<mongoid>', methods=['POST'])
def edit_post(mongoid):
    db.all_reviews.update_one({'_id': ObjectId(mongoid)}, {'$set': {
        'name': request.form['name'],
        'title': request.form['title'],
        'review': request.form['review'],
        'updated_at': datetime.now()
    }})
    return redirect(url_for('reviews'))

@app.route('/delete/<mongoid>', methods=['GET'])
def delete(mongoid):
    review = db.all_reviews.find_one({'_id': ObjectId(mongoid)})
    return render_template('delete.html', doc=review)

@app.route('/delete/<mongoid>', methods=['POST'])
def delete_post(mongoid):
    db.all_reviews.delete_one({'_id': ObjectId(mongoid)})
    return redirect(url_for('reviews'))

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error='Page not found'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('error.html', error='Internal server error'), 500

if __name__ == '__main__':
    app.run(debug=True)
