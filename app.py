from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ice_cream.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret_key'
db = SQLAlchemy(app)

# Models
class Flavor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    seasonal = db.Column(db.Boolean, default=False)
    ingredients = db.relationship('Ingredient', secondary='flavor_ingredients')

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

class AllergyConcern(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

class FlavorIngredients(db.Model):
    flavor_id = db.Column(db.Integer, db.ForeignKey('flavor.id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)

# Routes
@app.route('/')
def index():
    flavors = Flavor.query.all()
    search_query = request.args.get('search')
    seasonal_filter = request.args.get('seasonal')

    # Apply search filter
    if search_query:
        flavors = Flavor.query.filter(Flavor.name.contains(search_query)).all()

    # Apply seasonal filter
    if seasonal_filter:
        flavors = Flavor.query.filter_by(seasonal=True).all()

    return render_template('index.html', flavors=flavors)

@app.route('/add_flavor', methods=['POST'])
def add_flavor():
    name = request.form['name']
    seasonal = 'seasonal' in request.form
    flavor = Flavor(name=name, seasonal=seasonal)
    db.session.add(flavor)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/suggest_flavor', methods=['POST'])
def suggest_flavor():
    name = request.form['name']
    flavor = Flavor.query.filter_by(name=name).first()
    if not flavor:
        flavor = Flavor(name=name)
        db.session.add(flavor)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/add_to_cart/<int:flavor_id>', methods=['GET'])
def add_to_cart(flavor_id):
    flavor = Flavor.query.get(flavor_id)
    if flavor:
        if 'cart' not in session:
            session['cart'] = [] 
        if flavor.id not in session['cart']:
            session['cart'].append(flavor.id) 
        session.modified = True
    return redirect(url_for('index'))

@app.route('/remove_from_cart/<int:flavor_id>', methods=['GET'])
def remove_from_cart(flavor_id):
    if 'cart' in session and flavor_id in session['cart']:
        session['cart'].remove(flavor_id)
        session.modified = True
    return redirect(url_for('view_cart'))

@app.route('/view_cart')
def view_cart():
    cart_items = []
    if 'cart' in session:
        cart_items = Flavor.query.filter(Flavor.id.in_(session['cart'])).all()
    return render_template('cart.html', cart_items=cart_items)

@app.route('/add_allergy', methods=['POST'])
def add_allergy():
    name = request.form['name']
    if not AllergyConcern.query.filter_by(name=name).first():
        allergy = AllergyConcern(name=name)
        db.session.add(allergy)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/add_ingredient', methods=['POST'])
def add_ingredient():
    name = request.form['name']
    if not Ingredient.query.filter_by(name=name).first():
        ingredient = Ingredient(name=name)
        db.session.add(ingredient)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/ingredients')
def ingredients():
    ingredients_list = Ingredient.query.all()
    return render_template('ingredients.html', ingredients=ingredients_list)

@app.route('/view_ingredients')
def view_ingredients():
    ingredients = Ingredient.query.all()
    return render_template('ingredients.html', ingredients=ingredients)

@app.route('/delete_flavor/<int:flavor_id>', methods=['GET'])
def delete_flavor(flavor_id):
    flavor = Flavor.query.get(flavor_id)
    if flavor:
        db.session.delete(flavor)
        db.session.commit()
    return redirect(url_for('index'))

# Run the app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
