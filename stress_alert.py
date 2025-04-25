from typing import List, Dict, Any
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

class StressAlertSystem:
    def __init__(self):
        # Alert thresholds
        self.STRESS_THRESHOLD = 0.3  # Mood score below this indicates stress
        self.BURNOUT_THRESHOLD = 0.2  # Mood score below this indicates potential burnout
        self.CONSECUTIVE_DAYS_THRESHOLD = 3  # Number of consecutive days to trigger alert
        
        # Email configuration
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.sender_password = os.getenv('SENDER_PASSWORD')
        
        # Recipients
        self.hr_email = os.getenv('HR_EMAIL')
        self.manager_email = os.getenv('MANAGER_EMAIL')

    def analyze_mood_history(self, mood_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze mood history to detect stress patterns
        """
        if not mood_history:
            return {'status': 'normal', 'message': 'Insufficient mood data'}
        
        # Calculate average mood score for the last week
        recent_moods = [record['mood_score'] for record in mood_history[-7:]]
        avg_mood = sum(recent_moods) / len(recent_moods)
        
        # Check for consecutive low mood days
        consecutive_low_days = 0
        for record in reversed(mood_history):
            if record['mood_score'] < self.STRESS_THRESHOLD:
                consecutive_low_days += 1
            else:
                break
        
        # Determine alert level
        if avg_mood < self.BURNOUT_THRESHOLD and consecutive_low_days >= self.CONSECUTIVE_DAYS_THRESHOLD:
            return {
                'status': 'critical',
                'message': 'Potential burnout detected',
                'avg_mood': avg_mood,
                'consecutive_low_days': consecutive_low_days
            }
        elif avg_mood < self.STRESS_THRESHOLD:
            return {
                'status': 'warning',
                'message': 'Elevated stress levels detected',
                'avg_mood': avg_mood,
                'consecutive_low_days': consecutive_low_days
            }
        else:
            return {
                'status': 'normal',
                'message': 'Mood levels within normal range',
                'avg_mood': avg_mood,
                'consecutive_low_days': consecutive_low_days
            }

    def send_alert(self, employee_data: Dict[str, Any], analysis_result: Dict[str, Any]) -> bool:
        """
        Send email alert to HR and manager if stress is detected
        """
        if analysis_result['status'] == 'normal':
            return False
            
        try:
            # Create email message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = f"{self.hr_email}, {self.manager_email}"
            msg['Subject'] = f"Employee Well-being Alert - {employee_data['name']}"
            
            # Email body
            body = f"""
            Employee Well-being Alert
            
            Employee: {employee_data['name']}
            Team: {employee_data['team']}
            Status: {analysis_result['status'].upper()}
            
            Analysis:
            - Average Mood Score: {analysis_result['avg_mood']:.2f}
            - Consecutive Low Mood Days: {analysis_result['consecutive_low_days']}
            - Alert Message: {analysis_result['message']}
            
            Recommended Actions:
            - Schedule a check-in meeting
            - Review workload and deadlines
            - Consider offering support resources
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            return True
            
        except Exception as e:
            print(f"Failed to send alert email: {str(e)}")
            return False

    def should_send_alert(self, analysis_result: Dict[str, Any]) -> bool:
        """
        Determine if an alert should be sent based on analysis results
        """
        return analysis_result['status'] in ['warning', 'critical']

    def get_recommended_actions(self, analysis_result: Dict[str, Any]) -> List[str]:
        """
        Generate recommended actions based on stress level
        """
        if analysis_result['status'] == 'critical':
            return [
                "Immediate HR intervention required",
                "Schedule urgent one-on-one meeting",
                "Review and adjust workload",
                "Offer professional counseling services",
                "Consider temporary workload reduction"
            ]
        elif analysis_result['status'] == 'warning':
            return [
                "Schedule check-in meeting",
                "Review current workload",
                "Offer stress management resources",
                "Monitor mood trends",
                "Consider flexible work arrangements"
            ]
        else:
            return [
                "Continue regular check-ins",
                "Monitor mood trends",
                "Maintain current support level"
            ] 