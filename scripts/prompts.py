"""
Narrative prompts and content for emotion-based game system.
"""

MOOD_ATMOSPHERES = {
    'joy': {
        'setting': 'a vibrant emerald forest with golden sunbeams piercing through lush canopy',
        'ambience': 'chirping birds, rustling leaves, and the sweet scent of blooming flowers',
        'mood_adjectives': ['energetic', 'optimistic', 'bouncy', 'radiant', 'cheerful']
    },
    'fear': {
        'setting': 'a dark, mist-shrouded woodland where twisted trees cast eerie shadows',
        'ambience': 'haunting whispers, creaking branches, and the distant howl of unknown creatures',
        'mood_adjectives': ['cautious', 'trembling', 'alert', 'nervous', 'wary']
    },
    'anger': {
        'setting': 'a blazing crimson realm where jagged rocks pierce a blood-red sky',
        'ambience': 'crackling flames, thunderous roars, and the heat of molten earth',
        'mood_adjectives': ['fierce', 'determined', 'burning', 'relentless', 'powerful']
    },
    'neutral': {
        'setting': 'a peaceful clearing under a calm azure sky with fluffy white clouds',
        'ambience': 'gentle breezes, distant waterfalls, and the quiet rustle of grass',
        'mood_adjectives': ['thoughtful', 'balanced', 'steady', 'focused', 'serene']
    }
}

EMOTION_CLASSIFIER_SYSTEM_PROMPT = "You are an expert emotion classifier. Respond with only one word."

NARRATIVE_GENERATOR_SYSTEM_PROMPT = "You are a master game narrator specializing in immersive, atmospheric storytelling for platformer games. Create vivid, emotional narratives that make players feel heroic."

EMOTION_EXTRACTION_PROMPT = """Analyze the emotional tone of this real-life experience and respond with EXACTLY ONE WORD from: joy, fear, anger, or neutral.

User's experience: "{user_text}"

Guidelines:
- joy: happiness, excitement, success, love, achievement
- fear: worry, anxiety, stress, nervousness, uncertainty  
- anger: frustration, rage, injustice, betrayal, irritation
- neutral: calm, mundane, thoughtful, balanced situations

Emotion:"""

NARRATIVE_GENERATION_PROMPT = """Create a concise, immersive 10-second game intro narrative (exactly 3 sentences, about 25-30 words total) that blends:

CHARACTER: A brave red fox with amber eyes and a fluffy tail
SETTING: {setting}
REAL EXPERIENCE: "{user_text}"

REQUIREMENTS:
- Write in second person ("you") addressing the fox
- Connect the user's real experience to the fox's motivation
- Make it feel like the start of an epic adventure
- Match the {emotion} emotional tone
- End with the fox ready to begin the platforming challenge
- Use atmospheric, game-like language
- EXACTLY 3 SENTENCES
- Keep it concise for 10-second narration

EMOTION-SPECIFIC GUIDANCE:
- Joy: Fox feels {joy_adjectives}, ready for a fun adventure
- Fear: Fox feels {fear_adjectives}, but determined to overcome challenges  
- Anger: Fox feels {anger_adjectives}, channeling energy into action
- Neutral: Fox feels {neutral_adjectives}, approaching with wisdom

Create a brief narrative that transforms the player's experience into the fox's epic journey:"""

FALLBACK_NARRATIVES = {
    'joy': "Celebrating your success, you bound into a sunlit forest. Golden coins sparkle ahead. Your adventure begins!",
    'fear': "Despite your worries, you step into misty shadows. Courage guides your paws. The challenge awaits!",
    'anger': "Fueled by determination, you charge into a crimson realm. Your strength will overcome all. Victory awaits!",
    'neutral': "Reflecting on your thoughts, you enter a peaceful clearing. Wisdom guides your path. The journey starts!"
}