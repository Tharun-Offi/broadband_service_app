from flask import Flask, render_template, request, redirect, url_for, flash, session
from modal import db, User, Subscription, Billing, Feedback
from datetime import date, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///broadband_service.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'
db.init_app(app)

# Initialize the database tables
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return render_template('home.html', user=user)
    return render_template('home.html', user=None)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        phone_number = request.form['phone_number']
        email = request.form['email']
        address = f"{request.form['door']}, {request.form['street']}, {request.form['area']}, {request.form['city']}, {request.form['pincode']}"
        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'danger')
        else:
            new_user = User(username, password, phone_number, email, address)
            db.session.add(new_user)
            db.session.commit()
            flash('User registered successfully!', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Invalid username or password!', 'danger')
    return render_template('login.html')

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        flash('Please log in first!', 'warning')
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    return render_template('profile.html', user=user)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('home'))

@app.route('/profile/edit', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' not in session:
        flash('Please log in first!', 'warning')
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    if request.method == 'POST':
        user.phone_number = request.form['phone_number']
        user.email = request.form['email']
        user.address = f"{request.form['door']}, {request.form['street']}, {request.form['area']}, {request.form['city']}, {request.form['pincode']}"
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))
    return render_template('edit_profile.html', user=user)

@app.route('/subscription/modify', methods=['GET', 'POST'])
def modify_subscription():
    if 'user_id' not in session:
        flash('Please log in first!', 'warning')
        return redirect(url_for('login'))
    user_id = session['user_id']
    subscriptions = Subscription.query.filter_by(user_id=user_id).all()
    if request.method == 'POST':
        subscription_id = request.form['subscription_id']
        new_plan_id = request.form['plan_id']
        subscription = Subscription.query.get(subscription_id)
        subscription.plan_id = new_plan_id
        subscription.start_date = date.today()
        subscription.end_date = date.today() + timedelta(days=30)
        db.session.commit()
        flash('Subscription modified successfully!', 'success')
        return redirect(url_for('profile'))
    return render_template('modify_subscription.html', subscriptions=subscriptions)

@app.route('/subscription/apply', methods=['GET', 'POST'])
def apply_subscription():
    if 'user_id' not in session:
        flash('Please log in first!', 'warning')
        return redirect(url_for('login'))
    if request.method == 'POST':
        user_id = session['user_id']
        plan_id = request.form['plan_id']
        new_subscription = Subscription(user_id=user_id, plan_id=plan_id)
        db.session.add(new_subscription)
        db.session.commit()
        flash('New subscription applied successfully!', 'success')
        return redirect(url_for('profile'))
    return render_template('apply_subscription.html')

if __name__ == '__main__':
    app.run(debug=True)
