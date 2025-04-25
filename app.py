from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///mood_tracker.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    team = db.Column(db.String(100))
    mood_history = db.relationship('MoodRecord', backref='employee', lazy=True)

class MoodRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    mood_score = db.Column(db.Float, nullable=False)
    emotion_type = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    source = db.Column(db.String(50))  # text, facial, or speech
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    difficulty_level = db.Column(db.Integer)  # 1-5 scale
    mood_suitability = db.Column(db.String(50))  # happy, neutral, stressed, etc.
    mood_records = db.relationship('MoodRecord', backref='task', lazy=True)

# Routes
@app.route('/api/mood', methods=['POST'])
def record_mood():
    data = request.json
    try:
        new_record = MoodRecord(
            employee_id=data['employee_id'],
            mood_score=data['mood_score'],
            emotion_type=data['emotion_type'],
            source=data['source']
        )
        db.session.add(new_record)
        db.session.commit()
        return jsonify({"message": "Mood recorded successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/tasks/recommend', methods=['GET'])
def recommend_tasks():
    employee_id = request.args.get('employee_id')
    if not employee_id:
        return jsonify({"error": "Employee ID is required"}), 400
    
    # Get latest mood
    latest_mood = MoodRecord.query.filter_by(employee_id=employee_id)\
        .order_by(MoodRecord.timestamp.desc()).first()
    
    if not latest_mood:
        return jsonify({"error": "No mood data found for employee"}), 404
    
    # Recommend tasks based on mood
    suitable_tasks = Task.query.filter_by(mood_suitability=latest_mood.emotion_type).all()
    return jsonify([{
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "difficulty_level": task.difficulty_level
    } for task in suitable_tasks])

@app.route('/api/analytics/team', methods=['GET'])
def team_analytics():
    team = request.args.get('team')
    if not team:
        return jsonify({"error": "Team name is required"}), 400
    
    # Get mood records for the team
    mood_records = db.session.query(MoodRecord)\
        .join(Employee)\
        .filter(Employee.team == team)\
        .all()
    
    # Basic analytics
    analytics = {
        "average_mood": sum(record.mood_score for record in mood_records) / len(mood_records),
        "total_records": len(mood_records),
        "mood_distribution": {}
    }
    
    for record in mood_records:
        analytics["mood_distribution"][record.emotion_type] = \
            analytics["mood_distribution"].get(record.emotion_type, 0) + 1
    
    return jsonify(analytics)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 