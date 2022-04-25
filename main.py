from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, validators, SubmitField, FloatField, SelectField
from wtforms.validators import DataRequired, Length, URL


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

##CREATE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cafes.db"
# Optional: But it will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##CREATE TABLE
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String, nullable=True)
    img_url = db.Column(db.String(250), nullable=True)
    location = db.Column(db.String, nullable=True)
    has_sockets = db.Column(db.Integer, nullable=True)
    has_toilet = db.Column(db.Integer, nullable=True)
    has_wifi = db.Column(db.Integer, nullable=True)
    can_take_calls = db.Column(db.Integer, nullable=True)
    seats = db.Column(db.String(250), nullable=True)
    coffee_price = db.Column(db.String(25), nullable=False)

    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Cafe {self.name}>'


class CafeForm(FlaskForm):
    name = StringField('Cafe name', validators=[DataRequired()])
    map_url = StringField('Map URL', validators=[DataRequired(), URL(message='This is not a valid URL.')])
    img_url = StringField('Image URL', validators=[DataRequired(), URL(message='This is not a valid URL.')])
    location = StringField('Location', validators=[DataRequired()])
    has_sockets = SelectField('Coffee rating', validators=[DataRequired()],
                              choices=[0, 1])
    has_toilet = SelectField('Coffee rating', validators=[DataRequired()],
                             choices=[0, 1])
    has_wifi = SelectField('Coffee rating', validators=[DataRequired()],
                           choices=[0, 1])
    can_take_calls = SelectField('Coffee rating', validators=[DataRequired()],
                                 choices=[0, 1])
    seats = StringField('Number of Seats', validators=[DataRequired()])
    coffee_price = StringField('Coffee Price (in GBP)', validators=[DataRequired()])

    submit = SubmitField('Submit')

# all Flask routes below
@app.route("/")
def home():
    all_cafes = db.session.query(Cafe).all()
    print(all_cafes)
    return render_template("index.html", cafes=all_cafes)


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    form.validate_on_submit()
    print("true")
    if form.validate_on_submit():
        new_cafe = Cafe(name=form.name.data, map_url=form.map_url.data,  img_url=form.img_url.data, location=form.location.data, has_sockets=form.has_sockets.data,  has_toilet=form.has_toilet.data,  has_wifi=form.has_wifi.data,  can_take_calls=form.can_take_calls.data,  seats=form.seats.data,  coffee_price=form.coffee_price.data)
        db.session.add(new_cafe)
        db.session.commit()

        return redirect(url_for('home'))
    return render_template('add.html', form=form)

@app.route('/delete-cafe/<id>')
def delete_cafe(id):
    cafe_id = id
    cafe_to_delete = Cafe.query.get(cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
