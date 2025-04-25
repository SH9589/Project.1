import cv2
import numpy as np
from transformers import pipeline
import face_recognition
from typing import Dict, Any

class EmotionDetector:
    def __init__(self):
        # Initialize text emotion classifier
        self.text_classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")
        
        # Load face detection model
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Emotion labels mapping
        self.emotion_labels = {
            'positive': ['happy', 'excited', 'content'],
            'negative': ['sad', 'angry', 'stressed'],
            'neutral': ['neutral', 'calm']
        }

    def detect_text_emotion(self, text: str) -> Dict[str, Any]:
        """Analyze text input for emotional content"""
        result = self.text_classifier(text)[0]
        return {
            'emotion': result['label'],
            'confidence': result['score'],
            'source': 'text'
        }

    def detect_facial_emotion(self, image_path: str) -> Dict[str, Any]:
        """Analyze facial expressions from image"""
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) == 0:
            return {'error': 'No face detected'}
        
        # For each face, detect emotion (simplified version)
        emotions = []
        for (x, y, w, h) in faces:
            face_img = gray[y:y+h, x:x+w]
            # Here you would typically use a more sophisticated model
            # This is a placeholder for demonstration
            emotion = 'neutral'  # Replace with actual emotion detection
            confidence = 0.8  # Replace with actual confidence score
            emotions.append({
                'emotion': emotion,
                'confidence': confidence,
                'source': 'facial'
            })
        
        return emotions[0] if emotions else {'error': 'No emotions detected'}

    def detect_speech_emotion(self, audio_path: str) -> Dict[str, Any]:
        """Analyze speech for emotional content"""
        # This is a placeholder - implement actual speech emotion detection
        # You would typically use a speech emotion recognition model here
        return {
            'emotion': 'neutral',
            'confidence': 0.7,
            'source': 'speech'
        }

    def get_mood_score(self, emotion_data: Dict[str, Any]) -> float:
        """Convert emotion detection results to a mood score (0-1)"""
        emotion = emotion_data['emotion'].lower()
        confidence = emotion_data['confidence']
        
        if emotion in self.emotion_labels['positive']:
            base_score = 0.8
        elif emotion in self.emotion_labels['negative']:
            base_score = 0.2
        else:
            base_score = 0.5
            
        return base_score * confidence

    def detect_emotion(self, text: str = None, image_path: str = None, audio_path: str = None) -> Dict[str, Any]:
        """Main method to detect emotion from multiple sources"""
        results = []
        
        if text:
            results.append(self.detect_text_emotion(text))
        if image_path:
            results.append(self.detect_facial_emotion(image_path))
        if audio_path:
            results.append(self.detect_speech_emotion(audio_path))
            
        if not results:
            return {'error': 'No input provided for emotion detection'}
            
        # Combine results (simple average for demonstration)
        mood_scores = [self.get_mood_score(r) for r in results if 'error' not in r]
        if not mood_scores:
            return {'error': 'No valid emotion detection results'}
            
        avg_score = sum(mood_scores) / len(mood_scores)
        
        return {
            'mood_score': avg_score,
            'emotion_type': 'positive' if avg_score > 0.6 else 'negative' if avg_score < 0.4 else 'neutral',
            'confidence': avg_score,
            'sources_used': [r['source'] for r in results if 'error' not in r]
        } 