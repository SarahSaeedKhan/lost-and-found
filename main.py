from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/lost and found'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(60))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_item = db.Column(db.String(255))
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relation('User')


@app.route('/add_item', methods=['POST'])
def add_item():
    user = User.query.filter_by(email=request.form['email']).first()
    if user is None:
        user = User(firstname=request.form['firstname'], email=request.form['email'],
                    password=request.form['password'])
    item = Item(name_item=request.form['name_item'], description=request.form['description'],
                user_id=request.form['user_id'])
    db.session.add(user)
    db.session.commit()
    db.session.add(item)
    db.session.commit()
    register = {
        'name': user.firstname,
        'email': user.email,
        'password': user.password,
        'item': item.name_item,
        'item_description': item.description

    }
    return {'user': register}


@app.route('/search_item', methods=['GET'])
def search():
    search_item = input('enter the item you need to search')
    items = Item.query.all()
    for item in items:
        if search_item in item.name_item:
            return {
                'item_id': item.id,
                'item_name': item.name_item,
                'item_description': item.description
            }
        return 'not found'



@app.route('/')
def index():
    return 'hey'


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

