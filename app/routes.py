from app import app, db
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import UserInfoForm, LoginForm
from app.models import User, Products, Cart


@app.route('/')
def index():
    
    product_1_info = {
        'name': "T-shirt",
        'price': 9.99,
        'description': "This is a blue shirt"
    }
    product_2_info = {
        'name': "Pants",
        'price': 19.99,
        'description': "This is yellow pants"
    }
    if current_user.is_authenticated:
        product_1 = Products("T-shirt", 9.99, "This is a blue shirt", current_user.id)
        product_2 = Products("Pants", 19.99, "This is yellow pants", current_user.id)
        product_3 = Products("T-shirt", 9.99, "This is a blue shirt", current_user.id)
        product_4 = Products("Pants", 19.99, "This is yellow pants", current_user.id)
        my_products = [product_1, product_2, product_3, product_4]

        for product in my_products:
            db.session.add(product)
        
        # Cart.query.filter(Cart == Cart).delete()
        db.session.commit()
        
        return render_template('index.html', products=my_products )
    else:
        return render_template('index.html' )


@app.route('/signup', methods=["GET", 'POST'])
def signup():
    signup_form = UserInfoForm()
    if signup_form.validate_on_submit():
        username = signup_form.username.data
        email = signup_form.email.data
        password = signup_form.password.data

        existing_user = User.query.filter_by(username=username).all()

        if existing_user:
            flash(f'The username {username} is already registered. Please try again.', 'danger')
            return redirect(url_for('register'))

        new_user = User(username, email, password)
        db.session.add(new_user)
        db.session.commit()
        flash(f'Thank you {username}, you have succesfully registered!', 'success')
        return redirect(url_for('index'))
        
    return render_template('signup.html', form=signup_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            flash('Your username or password is incorrect', 'danger')
            return redirect(url_for('login'))
        
        login_user(user)
        flash(f'Welcome {user.username}. You have succesfully logged in.', 'success')

        return redirect(url_for('index'))
        
    return render_template('login.html', login_form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/my-account')
@login_required
def my_account():
    return render_template('my_account.html')

@app.route('/my_cart')
@login_required
def my_cart():
    item = Cart.query.all()
    total = []
    for i in item:
        total.append(i.price)
        total1 = sum(total)
    return render_template('my_cart.html', item=item, total1=total1)

@app.route('/product_page/<int:product_id>')
@login_required
def product_page(product_id):
    product = Products.query.get_or_404(product_id)
    return render_template('product_page.html', product=product)


@app.route('/product_page/<int:product_id>/cart', methods=['POST'])
@login_required
def add_cart(product_id):
    product = Products.query.get_or_404(product_id)
    new_cart = Cart(product.name, product.price, current_user.id, product_id)
    db.session.add(new_cart)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/my_cart/<int:product_id>/cart_item', methods=['POST'])
@login_required
def delete_cart(product_id):
    Cart.query.filter(Cart.id == product_id).delete()
    db.session.commit()
    return redirect(url_for('index'))
