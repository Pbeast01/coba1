from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Database setup
DATABASE = 'confession.db'

def init_db():
    """Initialize the database."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS responses (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            response TEXT NOT NULL
                        )''')
        conn.commit()

@app.route('/')
def home():
    """Render the homepage."""
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    """Handle form submission."""
    name = request.form['name']
    response = request.form['response']

    # Save to database
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO responses (name, response) VALUES (?, ?)", (name, response))
        conn.commit()

    # Redirect to thank you page
    return render_template('thanks.html', name=name, response=response)

@app.route('/responses')
def view_responses():
    """View all responses."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, response FROM responses")
        data = cursor.fetchall()

    return render_template('responses.html', data=data)

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)
