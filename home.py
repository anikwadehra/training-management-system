import json
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime, timedelta
import calendar

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this to a secure secret key

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Load user data from JSON file
def load_users():
    with open('users.json') as f:
        data = json.load(f)
    return {user['user_name']: {'password': user['password'], 'user_id': user['user_id'], 'user_type': user['user_type']} for user in data['users']}

users = load_users()  # Load users from JSON

class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id
        
@login_manager.user_loader
def load_user(user_id):
    for username, details in users.items():
        if details['user_id'] == user_id:
            return User(user_id)
    return None

@app.route('/home', methods=['GET', 'POST'])
@login_required  # Ensure user is logged in
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if email in users and users[email]['password'] == password:
            user = User(users[email]['user_id'])  # Use user_id for login
            login_user(user)
            print('Logged in successfully.')
            return redirect(url_for('home'))  # Redirect to home after login
        else:
            print('Invalid email or password.')
    
    return render_template('login.html')

@app.route('/logout', methods=['POST'])  # Ensure only POST requests are allowed
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/calendar', methods=['GET', 'POST'])
@login_required
def get_calendar_data():
    # Load existing training sessions
    try:
        with open('trainings.json') as f:
            trainings = json.load(f)
    except FileNotFoundError:
        trainings = []

    # Get the current month and year from the request or default to the current date
    month = request.args.get('month', default=datetime.now().month, type=int)
    year = request.args.get('year', default=datetime.now().year, type=int)

    # Create a calendar for the specified month and year
    cal = calendar.Calendar(firstweekday=calendar.SUNDAY)
    month_days = cal.monthdayscalendar(year, month)

    # Prepare the calendar data
    calendar_data = []
    for week in month_days:
        week_data = []
        for day in week:
            if day == 0:
                week_data.append({'day': '', 'date': ''})  # Empty day
            else:
                date_str = f"{year}-{month:02d}-{day:02d}"
                week_data.append({'day': day, 'date': date_str})  # Day and date
        calendar_data.append(week_data)

    if request.method == 'POST':
        # Add a new training session
        new_training = {
            'title': request.form['title'],
            'date': request.form['date'],
            'time': request.form['time']
        }
        trainings.append(new_training)

        # Save the updated training sessions to the JSON file
        with open('trainings.json', 'w') as f:
            json.dump(trainings, f)

        return redirect(url_for('get_calendar_data', month=month, year=year))

    return render_template('calendar.html', trainings=trainings, calendar=calendar_data, current_month=calendar.month_name[month] + " " + str(year))

if __name__ == '__main__':
    app.run(host='192.168.31.153',debug=True, port=5001)
    # Install required packages
    # Run these commands in your terminal:
    # pip install flask
    # pip install flask-login
    # pip install werkzeug
