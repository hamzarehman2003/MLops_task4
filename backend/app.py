from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Function to establish a connection to PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        host="db",              # The service name for PostgreSQL as defined in docker-compose.yml
        database="gpa_db",       # Database name
        user="gpa_user",         # User
        password="password123"   # Password
    )
    return conn

# Initialize the database with a "students" table
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            gpa REAL NOT NULL
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

@app.route('/calculate', methods=['POST'])
def calculate_gpa():
    data = request.get_json()
    grades = data.get('grades')

    if not grades or len(grades) == 0:
        return jsonify({'error': 'No grades provided'}), 400

    gpa = sum(grades) / len(grades)
    return jsonify({'gpa': gpa})

@app.route('/save', methods=['POST'])
def save_gpa():
    data = request.get_json()
    name = data.get('name')
    gpa = data.get('gpa')

    if not name or not gpa:
        return jsonify({'error': 'Name or GPA missing'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO students (name, gpa) VALUES (%s, %s)', (name, gpa))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'GPA saved successfully'}), 201

if __name__ == '__main__':
    init_db()   # Initialize the database when the app starts
    app.run(host='0.0.0.0', port=5000)
