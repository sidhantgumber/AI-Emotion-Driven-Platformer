"""
Clean OpenAI-based emotion detection and narrative generation system.
"""

import os
from openai import OpenAI
from prompts import (
    MOOD_ATMOSPHERES, 
    EMOTION_CLASSIFIER_SYSTEM_PROMPT,
    NARRATIVE_GENERATOR_SYSTEM_PROMPT,
    EMOTION_EXTRACTION_PROMPT,
    NARRATIVE_GENERATION_PROMPT,
    FALLBACK_NARRATIVES
)

class EmotionBrain:
    def __init__(self, api_key=None):
        # Get API key from environment variable or parameter
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found. Please set the OPENAI_API_KEY environment variable "
                "or pass the api_key parameter to EmotionBrain()"
            )
        
        self.client = OpenAI(api_key=self.api_key)
        print("Emotion Brain initialized with API key from environment")
    
    def extract_emotion(self, user_text, model="gpt-3.5-turbo"):
        """Extract primary emotion from user's real-life experience."""
        prompt = EMOTION_EXTRACTION_PROMPT.format(user_text=user_text)
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": EMOTION_CLASSIFIER_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=5,
                temperature=0.1
            )
            
            emotion = response.choices[0].message.content.strip().lower()
            
            if emotion not in ['joy', 'fear', 'anger', 'neutral']:
                emotion = 'neutral'
                
            print(f"Detected emotion: {emotion}")
            return emotion
            
        except Exception as e:
            print(f"Emotion extraction error: {e}")
            return 'neutral'
    
    def generate_narrative(self, user_text, emotion, model="gpt-3.5-turbo"):
        """Generate an immersive narrative for the red fox character."""
        atmosphere = MOOD_ATMOSPHERES.get(emotion, MOOD_ATMOSPHERES['neutral'])
        
        prompt = NARRATIVE_GENERATION_PROMPT.format(
            setting=atmosphere['setting'],
            ambience=atmosphere['ambience'],
            user_text=user_text,
            emotion=emotion,
            joy_adjectives=', '.join(MOOD_ATMOSPHERES['joy']['mood_adjectives'][:3]),
            fear_adjectives=', '.join(MOOD_ATMOSPHERES['fear']['mood_adjectives'][:3]),
            anger_adjectives=', '.join(MOOD_ATMOSPHERES['anger']['mood_adjectives'][:3]),
            neutral_adjectives=', '.join(MOOD_ATMOSPHERES['neutral']['mood_adjectives'][:3])
        )
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": NARRATIVE_GENERATOR_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=120,
                temperature=0.8
            )
            
            narrative = response.choices[0].message.content.strip()
            narrative = narrative.replace('"', '').replace('*', '').strip()
            
            print(f"Generated narrative: {narrative}")
            return narrative
            
        except Exception as e:
            print(f"Narrative generation error: {e}")
            return self._get_fallback_narrative(user_text, emotion)
    
    def _get_fallback_narrative(self, user_text, emotion):
        """Get fallback narrative if API fails."""
        template = FALLBACK_NARRATIVES.get(emotion, FALLBACK_NARRATIVES['neutral'])
        return template.format(user_text=user_text.lower())
    
    def process_user_input(self, user_text, model="gpt-3.5-turbo"):
        """Main function: Transform user experience into game data."""
        print(f"Processing: '{user_text}'")
        
        emotion = self.extract_emotion(user_text, model)
        narrative = self.generate_narrative(user_text, emotion, model)
        
        result = {
            'emotion': emotion,
            'narrative': narrative,
            'user_input': user_text,
            'atmosphere': MOOD_ATMOSPHERES[emotion],
            'background_theme': emotion
        }
        
        return result
    
    def get_atmosphere_description(self, emotion):
        """Get atmospheric description for UI display."""
        atmosphere = MOOD_ATMOSPHERES.get(emotion, MOOD_ATMOSPHERES['neutral'])
        return atmosphere['setting']


def main():
    """Test the emotion brain system."""
    print("Testing Emotion Brain System")
    print("=" * 40)
    
    brain = EmotionBrain()
    
    test_cases = [
        "I drank a glass of water"
    ]
    
    print("\nTesting emotion detection and narrative generation:")
    print("-" * 50)
    
    for case in test_cases:
        print(f"\nInput: {case}")
        result = brain.process_user_input(case)
        print(f"Emotion: {result['emotion'].upper()}")
        print(f"Narrative: {result['narrative']}")
        print("-" * 50)


# if __name__ == "__main__":
#     main()
