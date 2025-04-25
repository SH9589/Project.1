from typing import List, Dict, Any
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class TaskRecommender:
    def __init__(self):
        # Task difficulty levels (1-5)
        self.difficulty_levels = {
            'very_easy': 1,
            'easy': 2,
            'medium': 3,
            'hard': 4,
            'very_hard': 5
        }
        
        # Mood to task difficulty mapping
        self.mood_difficulty_mapping = {
            'positive': ['very_hard', 'hard', 'medium'],
            'neutral': ['medium', 'easy'],
            'negative': ['easy', 'very_easy']
        }
        
        # Sample task database (in production, this would be in a database)
        self.tasks = [
            {
                'id': 1,
                'title': 'Code Review',
                'description': 'Review and provide feedback on team member\'s code',
                'difficulty_level': 3,
                'mood_suitability': 'neutral',
                'tags': ['technical', 'collaboration']
            },
            {
                'id': 2,
                'title': 'Bug Fixing',
                'description': 'Fix critical production bugs',
                'difficulty_level': 4,
                'mood_suitability': 'positive',
                'tags': ['technical', 'urgent']
            },
            {
                'id': 3,
                'title': 'Documentation',
                'description': 'Update project documentation',
                'difficulty_level': 2,
                'mood_suitability': 'negative',
                'tags': ['writing', 'organization']
            },
            {
                'id': 4,
                'title': 'Team Meeting',
                'description': 'Participate in team standup meeting',
                'difficulty_level': 1,
                'mood_suitability': 'negative',
                'tags': ['communication', 'collaboration']
            },
            {
                'id': 5,
                'title': 'Feature Development',
                'description': 'Implement new feature based on specifications',
                'difficulty_level': 5,
                'mood_suitability': 'positive',
                'tags': ['technical', 'development']
            }
        ]

    def get_recommended_tasks(self, mood_data: Dict[str, Any], num_recommendations: int = 3) -> List[Dict[str, Any]]:
        """
        Recommend tasks based on employee's current mood
        """
        mood_score = mood_data['mood_score']
        emotion_type = mood_data['emotion_type']
        
        # Filter tasks based on mood suitability
        suitable_tasks = [
            task for task in self.tasks 
            if task['mood_suitability'] == emotion_type
        ]
        
        if not suitable_tasks:
            # If no exact match, find closest mood suitability
            suitable_tasks = self.tasks
        
        # Sort tasks by difficulty level appropriate for the mood
        if emotion_type == 'positive':
            suitable_tasks.sort(key=lambda x: x['difficulty_level'], reverse=True)
        elif emotion_type == 'negative':
            suitable_tasks.sort(key=lambda x: x['difficulty_level'])
        else:  # neutral
            suitable_tasks.sort(key=lambda x: abs(x['difficulty_level'] - 3))
        
        # Return top N recommendations
        return suitable_tasks[:num_recommendations]

    def get_task_difficulty_for_mood(self, mood_score: float) -> List[str]:
        """
        Determine appropriate task difficulty levels based on mood score
        """
        if mood_score > 0.7:
            return self.mood_difficulty_mapping['positive']
        elif mood_score < 0.3:
            return self.mood_difficulty_mapping['negative']
        else:
            return self.mood_difficulty_mapping['neutral']

    def calculate_task_suitability(self, task: Dict[str, Any], mood_data: Dict[str, Any]) -> float:
        """
        Calculate how suitable a task is for the current mood
        """
        mood_score = mood_data['mood_score']
        task_difficulty = task['difficulty_level']
        
        # Normalize task difficulty to 0-1 scale
        normalized_difficulty = (task_difficulty - 1) / 4.0
        
        # Calculate suitability score (higher is better)
        if mood_score > 0.7:  # Positive mood
            suitability = 1.0 - abs(normalized_difficulty - 0.75)
        elif mood_score < 0.3:  # Negative mood
            suitability = 1.0 - abs(normalized_difficulty - 0.25)
        else:  # Neutral mood
            suitability = 1.0 - abs(normalized_difficulty - 0.5)
            
        return max(0.0, min(1.0, suitability)) 