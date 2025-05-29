from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from modal import db, User, Subscription, Billing, Feedback, Admin, Plan  # Import Admin and Plan models
from datetime import date, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///broadband_service.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'
db.init_app(app)

# Initialize the database tables
with app.app_context():
    db.create_all()

# Create a default admin account if it doesn't exist
with app.app_context():
    if not Admin.query.filter_by(username='admin').first():
        default_admin = Admin(username='admin', password='Admin@123')
        db.session.add(default_admin)
        db.session.commit()

@app.route('/')
def home():
    plans = Plan.query.all()
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return render_template('home.html', user=user, plans=plans)
    elif 'admin_id' in session:
        admin = Admin.query.get(session['admin_id'])
        if admin.username == 'admin':  # Default admin
            return redirect(url_for('admin_dashboard'))
        else:  # Promoted admin
            user = User.query.filter_by(username=admin.username).first()
            return render_template('home.html', user=user, plans=plans, is_admin=True)
    return render_template('home.html', user=None, plans=plans)

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
        elif User.query.filter_by(email=email).first():
            flash('Email already exists!', 'danger')
        elif User.query.filter_by(phone_number=phone_number).first():
            flash('Phone number already exists!', 'danger')
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

        # Check if the credentials match an admin
        admin = Admin.query.filter_by(username=username, password=password).first()
        if admin:
            session['admin_id'] = admin.id
            flash('Admin login successful!', 'success')
            return redirect(url_for('admin_dashboard'))

        # Check if the credentials match a user
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            flash('User login successful!', 'success')
            return redirect(url_for('home'))

        # If no match, show an error
        flash('Invalid username or password!', 'danger')
    return render_template('login.html')

@app.route('/profile', defaults={'user_id': None}, methods=['GET'])
@app.route('/profile/<int:user_id>', methods=['GET'])
def profile(user_id):
    if 'user_id' in session:
        # Regular user viewing their own profile
        user = User.query.get(session['user_id'])
        if user_id is None or user_id == user.id:
            return render_template('profile.html', user=user, is_admin=False)
        else:
            flash('You cannot view other profiles!', 'warning')
            return redirect(url_for('home'))
    elif 'admin_id' in session:
        admin = Admin.query.get(session['admin_id'])
        if admin.username == 'admin':  # Default admin cannot access user profile page
            flash('Default admin cannot access user profiles!', 'warning')
            return redirect(url_for('admin_dashboard'))
        else:  # Promoted admins can only view their own profile here
            if user_id is None or User.query.get(user_id).username == admin.username:
                user = User.query.filter_by(username=admin.username).first()
                return render_template('profile.html', user=user, is_admin=True)
            else:
                flash('You cannot view other profiles here!', 'warning')
                return redirect(url_for('home'))
    else:
        flash('Please log in first!', 'warning')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('admin_id', None)
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
        # Prevent duplicate subscriptions for the same plan
        existing = Subscription.query.filter_by(user_id=user_id, plan_id=plan_id).first()
        if existing:
            flash('You have already subscribed to this plan!', 'info')
        else:
            new_subscription = Subscription(user_id=user_id, plan_id=plan_id)
            db.session.add(new_subscription)
            db.session.commit()
            flash('New subscription applied successfully!', 'success')
        return redirect(url_for('profile'))
    return render_template('apply_subscription.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin_id' not in session:
        flash('Please log in as admin first!', 'warning')
        return redirect(url_for('admin_login'))
    admin = Admin.query.get(session['admin_id'])
    if admin.username == 'admin':  # Default admin can see all users
        users = User.query.all()
    else:
        admin_usernames = [a.username for a in Admin.query.all()]
        users = User.query.filter(
            (~User.username.in_(admin_usernames)) | (User.username == admin.username)
        ).all()
    plans = Plan.query.all()
    return render_template('admin_dashboard.html', users=users, plans=plans)

@app.route('/admin/add_plan', methods=['GET', 'POST'])
def add_plan():
    if 'admin_id' not in session:
        flash('Please log in as admin first!', 'warning')
        return redirect(url_for('admin_login'))
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        speed = request.form['speed']
        data_limit = request.form['data_limit']
        offer = request.form.get('offer', '')  # Get the offer field
        new_plan = Plan(name, price, speed, data_limit, offer)
        db.session.add(new_plan)
        db.session.commit()
        flash('Plan added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('add_plan.html')

@app.route('/admin/edit_plan/<int:plan_id>', methods=['GET', 'POST'])
def edit_plan(plan_id):
    if 'admin_id' not in session:
        flash('Please log in as admin first!', 'warning')
        return redirect(url_for('admin_login'))
    plan = Plan.query.get(plan_id)
    if request.method == 'POST':
        plan.name = request.form['name']
        plan.price = request.form['price']
        plan.speed = request.form['speed']
        plan.data_limit = request.form['data_limit']
        plan.offer = request.form.get('offer', '')  # Update the offer field
        db.session.commit()
        flash('Plan updated successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('edit_plan.html', plan=plan)

@app.route('/admin/delete_plan/<int:plan_id>', methods=['POST'])
def delete_plan(plan_id):
    if 'admin_id' not in session:
        flash('Please log in as admin first!', 'warning')
        return redirect(url_for('admin_login'))
    plan = Plan.query.get(plan_id)
    db.session.delete(plan)
    db.session.commit()
    flash('Plan deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/search_users', methods=['GET'])
def search_users():
    if 'admin_id' not in session:
        flash('Please log in as admin first!', 'warning')
        return redirect(url_for('admin_login'))
    query = request.args.get('query', '')
    plan_filter = request.args.get('plan_filter', '')
    admin = Admin.query.get(session['admin_id'])
    admin_usernames = [a.username for a in Admin.query.all()]
    # Always include the current admin in the search results, even if they are a promoted admin
    users = User.query.filter(
        (
            (User.username.contains(query)) |
            (User.phone_number.contains(query)) |
            (User.email.contains(query))
        ) &
        (
            (~User.username.in_(admin_usernames)) | (User.username == admin.username)
        )
    ).all()
    if plan_filter:
        users = [user for user in users if Subscription.query.filter_by(user_id=user.id, plan_id=plan_filter).first()]
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify([
            {
                'id': user.id,
                'username': user.username,
                'phone_number': user.phone_number,
                'email': user.email,
                'address': user.address
            } for user in users
        ])
    plans = Plan.query.all()
    return render_template('search_users.html', users=users, plans=plans, query=query, plan_filter=plan_filter)

@app.route('/admin/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if 'admin_id' not in session:
        flash('Please log in as admin first!', 'warning')
        return redirect(url_for('admin_login'))
    user = User.query.get(user_id)
    if request.method == 'POST':
        user.phone_number = request.form['phone_number']
        user.email = request.form['email']
        user.address = request.form['address']
        db.session.commit()
        flash('User details updated successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('edit_user.html', user=user)

@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if 'admin_id' not in session:
        flash('Please log in as admin first!', 'warning')
        return redirect(url_for('admin_login'))
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/promote/<int:user_id>', methods=['POST'])
def promote_to_admin(user_id):
    if 'admin_id' not in session:
        flash('Please log in as admin first!', 'warning')
        return redirect(url_for('admin_login'))
    user = User.query.get(user_id)
    if user:
        if Admin.query.filter_by(username=user.username).first():
            flash(f'User {user.username} is already an admin!', 'warning')
        else:
            new_admin = Admin(username=user.username, password=user.password)
            db.session.add(new_admin)
            db.session.commit()
            flash(f'User {user.username} has been promoted to admin!', 'success')
    else:
        flash('User not found!', 'danger')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/demote/<int:user_id>', methods=['POST'])
def demote_from_admin(user_id):
    if 'admin_id' not in session:
        flash('Please log in as admin first!', 'warning')
        return redirect(url_for('admin_login'))
    user = User.query.get(user_id)
    if user:
        admin = Admin.query.filter_by(username=user.username).first()
        if admin:
            db.session.delete(admin)
            db.session.commit()
            flash(f'Admin {user.username} has been demoted to a regular user!', 'success')
        else:
            flash(f'User {user.username} is not an admin!', 'warning')
    else:
        flash('User not found!', 'danger')
    return redirect(url_for('admin_dashboard'))

@app.context_processor
def inject_models():
    return dict(Admin=Admin)

if __name__ == '__main__':
    app.run(debug=True)
