from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required, current_user, logout_user, AnonymousUserMixin
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

# app and database initialization
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-drynex-website.db'
app.config['SECRET_KEY'] = 'fn89hfn23un28nf91n89nd2983fn9823fn8'
db = SQLAlchemy(app)

# admin initialization
admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')


# models for website
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    orders = db.relationship('Cart', backref='user', lazy=True)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unique_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    offer_price = db.Column(db.Float, nullable=True)
    img_url = db.Column(db.String(255), nullable=True)


# use of admin view over Product model
admin.add_view(ModelView(Product, db.session))


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unique_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    offer_price = db.Column(db.Float, nullable=True)
    img_url = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# with app.app_context():
#     db.create_all()


@app.route('/')
def home():
    response = Product.query.all()
    return render_template('index.html',products=response)


@app.route('/shop')
def shop_page():
    response = Product.query.all()
    return render_template('shop.html',products=response)


@app.route('/product/<unique_id>')
def show_product(unique_id):
    # response = Product.query.all()
    final_product=None
    response=Product.query.all()
    for products in response:
        if products.unique_id==unique_id:
            final_product=products
    return render_template('product.html',product=final_product,all_products=response)


@app.route('/add-cart/<unique_id>')
def add_to_cart(unique_id):
    final_product = None
    response = Product.query.all()
    for products in response:
        if products.unique_id == unique_id:
            final_product = products
    unique_id = final_product.unique_id
    name = final_product.name
    price = final_product.price
    offer_price = final_product.offer_price
    img_url = final_product.img_url
    user_id = 1  # Replace with the actual user ID (you may get it from the current user)

    # Create a new Cart entry
    new_cart_item = Cart(unique_id=unique_id, name=name, price=price, offer_price=offer_price, img_url=img_url,
                         user_id=user_id+1)

    # Add the new entry to the database
    db.session.add(new_cart_item)
    db.session.commit()
    final_product = None
    response = Product.query.all()
    for products in response:
        if products.unique_id == unique_id:
            final_product = products
    return render_template('product.html',product=final_product,all_products=response)


@app.route('/update-cart')
def update_cart():
    Cart.query.group_by()
    Cart.query.delete()
    db.session.commit()
    total = 0
    response = Product.query.all()
    print(response)
    for items in response:
        total += items.offer_price
    return redirect(url_for('cart_page', total=total))


@app.route('/cart')
def cart_page():
    total = 0
    response = Cart.query.all()
    for items in response:
        total += items.offer_price
    return render_template('shoping-cart.html',items=response,total=total)


@app.route('/sign-in')
def sign_in_page():
    return "working"


if __name__ == "__main__":
    app.run(debug=True)


