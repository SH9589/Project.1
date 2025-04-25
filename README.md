# AI-Powered Task Optimizer

An intelligent system that analyzes employee emotions and moods using multiple data sources (text, facial expressions, and speech) to optimize task assignments and enhance workplace well-being.

## Features

- **Real-Time Emotion Detection**
  - Text analysis for emotional content
  - Facial expression recognition
  - Speech emotion analysis
  - Multi-source emotion fusion

- **Smart Task Recommendations**
  - Mood-based task assignment
  - Difficulty level optimization
  - Personalized task suggestions

- **Historical Mood Tracking**
  - Individual mood timeline
  - Pattern recognition
  - Long-term well-being insights

- **Stress Management Alerts**
  - Automated HR notifications
  - Burnout detection
  - Proactive intervention system

- **Team Analytics**
  - Team mood aggregation
  - Productivity trend analysis
  - Morale monitoring

- **Data Privacy**
  - Secure data storage
  - Anonymized analytics
  - Compliance with privacy standards

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Git

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-task-optimizer.git
cd ai-task-optimizer
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with the following variables:
```env
DATABASE_URL=sqlite:///mood_tracker.db
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
HR_EMAIL=hr@company.com
MANAGER_EMAIL=manager@company.com
```

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. The API endpoints will be available at `http://localhost:5000`:

### API Endpoints

- **Record Mood**
  ```
  POST /api/mood
  ```
  Records an employee's mood with text, facial, or speech data.

- **Get Task Recommendations**
  ```
  GET /api/tasks/recommend?employee_id=<id>
  ```
  Returns personalized task recommendations based on current mood.

- **Team Analytics**
  ```
  GET /api/analytics/team?team=<team_name>
  ```
  Provides team-wide mood analytics and trends.

## Project Structure

```
ai-task-optimizer/
├── app.py                 # Main Flask application
├── emotion_detector.py    # Emotion detection module
├── task_recommender.py    # Task recommendation system
├── stress_alert.py        # Stress monitoring and alerts
├── requirements.txt       # Project dependencies
└── .env                  # Environment variables
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenCV for facial recognition
- Transformers library for text analysis
- Flask for web framework
- SQLAlchemy for database management

## Support

For support, email support@company.com or create an issue in the repository. 