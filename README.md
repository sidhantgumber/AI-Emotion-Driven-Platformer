# AI Emotion-Based Platformer Game

An innovative 2D platformer that uses artificial intelligence to analyze your real-life experiences and dynamically generate personalized game levels based on your emotional state. Experience your feelings through gameplay as a brave red fox navigating emotionally-tuned worlds. Every time you enter what you're feeling, the game procedurally generates a new level with a custom curated narrative audio. Collect coins and reach the end of the level! 



## Core Concept

1. **Share Your Experience**: Describe what happened in your day (e.g., "I got promoted!" or "Traffic was terrible")
2. **AI Emotion Analysis**: OpenAI GPT analyzes your text to detect emotion (joy, fear, anger, neutral)
3. **Dynamic Level Generation**: Procedural algorithms create a platformer level that reflects your detected emotion
4. **Immersive Narrative**: AI generates a personalized story connecting your experience to the fox's adventure
5. **Audio Narration**: High-quality text-to-speech brings your story to life
6. **Emotional Gameplay**: Navigate through levels that physically manifest your feelings

## Quick Start

### Prerequisites
- Python 3.10 (Reccomended)
- OpenAI API key (for emotion detection and narrative generation)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sidhantgumber/AI-Emotion-Driven-Platformer.git
   cd FinalProject
   ```

2. **Install dependencies**
   ```bash
   conda create --name myenv python=3.10 
   conda activate myenv  
   ```   

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up OpenAI API key**
   - Get your API key from [OpenAI](https://platform.openai.com/api-keys)
   - Add your key as an environment variable or in EmotionBrain() to be recognized by the script `scripts/ml_agents.py` (line 17)

5. **Run the game**
   ```bash
   cd scripts
   python game.py
   ```

### Game Controls
- **WASD/Arrow Keys**: Move and jump
- **SPACE/W/UP**: Jump
- **R**: New experience (restart when lost or return to input for a new experience when pressing mid game)
- **S**: Skip/stop narration
- **ESC**: Quit game

### Objective
Collect **5 coins** and reach the **pirate hat** to win! Your movement physics change based on your detected emotion.

## AI-Powered Emotion System

### Emotion Detection
The AI analyzes your input and classifies it into four core emotions:

| Emotion | Examples | Level Characteristics |
|---------|----------|----------------------|
| **Joy** | "Got promoted!", "Beautiful sunset", "Had a great date" | Bouncy physics, long platforms, abundant collectibles |
| **Fear** | "Job interview tomorrow", "Heard strange noises", "Feeling anxious" | Heavy physics, short platforms, sparse rewards |
| **Anger** | "Traffic jam!", "Unfair treatment", "Broken promises" | Aggressive physics, chaotic layout, challenging jumps |
| **Neutral** | "Normal day", "Drank water", "Watched TV" | Balanced physics, standard platforming |

### Dynamic Physics System
Your fox character's movement adapts to your emotion:

- **Joy**: Light (gravity: 0.4), fast (speed: 6), high jumps (-16), bouncy animations
- **Fear**: Heavy (gravity: 1.3), slow (speed: 4), powerful jumps (-20), cautious animations  
- **Anger**: Intense (gravity: 1.3), very fast (speed: 9), explosive jumps (-28), rapid animations
- **Neutral**: Balanced (gravity: 0.9), moderate (speed: 5), standard jumps (-20), normal animations

## Architecture & Technical Details

### Core Systems

#### Procedural Level Generation (`level_generator.py`)
- **Emotion-Based Parameters**: Each emotion has unique platform lengths, gap sizes, and decoration density
- **Intelligent Platform Placement**: Ensures playable paths while maintaining emotional character
- **Multi-Layer Generation**: Terrain, decorations, collectibles, and spawn points generated separately
- **CSV Export System**: Levels saved in modular format for easy loading and modification

#### AI Integration (`ml_agents.py`)
- **OpenAI GPT-3.5 Integration**: Robust emotion classification and narrative generation
- **Structured Prompts**: Carefully crafted prompts ensure consistent, high-quality outputs
- **Fallback Systems**: Local narratives when API is unavailable
- **Error Handling**: Graceful degradation with meaningful error messages

#### Audio System (`audio_manager.py`, `tts.py`)
- **Emotion-Specific Music**: Background tracks that match detected emotions
- **Edge-TTS Integration**: High-quality Microsoft voices for narrative narration
- **Dynamic Sound Effects**: Jump, coin collection, death, and victory sounds
- **Volume Management**: Separate controls for music and sound effects

#### Player System (`player.py`)
- **Emotion-Adaptive Physics**: Movement parameters change based on detected emotion
- **State Management**: Handles death, respawn, win conditions, and score tracking
- **Collision Detection**: Precise tile-based collision with terrain
- **Animation System**: Smooth sprite animations for idle, run, jump, and fall states

#### Rendering System (`level_viewer.py`)
- **Layered Rendering**: Background → terrain → decorations → player → UI
- **Viewport Culling**: Only renders visible tiles for optimal performance
- **Camera System**: Smooth interpolation following player movement
- **Emotion-Specific Backgrounds**: Dynamic sky colors and textures

## Emotion-Based Level Design

### Joy Levels 
- **Atmosphere**: Vibrant emerald forest with golden sunbeams
- **Platforms**: Long (6-12 tiles), encouraging exploration
- **Gaps**: Small (3-5 tiles), easily jumpable
- **Floating Platforms**: Abundant (55% chance), creating vertical playground
- **Decorations**: Lush grass (95% coverage), many trees (22% chance)
- **Collectibles**: Generous (60% chance), rewarding exploration
- **Sky**: Bright yellow-to-blue gradient
- **Music**: Upbeat, energetic background track

### Fear Levels 
- **Atmosphere**: Dark, mist-shrouded woodland with eerie shadows
- **Platforms**: Very short (2-3 tiles), creating uncertainty
- **Gaps**: Minimal (1-2 tiles), focusing on ground-level navigation
- **Floating Platforms**: Rare (10% chance), keeping player grounded
- **Decorations**: Sparse grass (55% coverage), few trees (8% chance)
- **Collectibles**: Scarce (30% chance), requiring careful exploration
- **Sky**: Dark blue-to-black gradient
- **Music**: Tense, atmospheric background track

### Anger Levels 
- **Atmosphere**: Blazing crimson realm with jagged rocks
- **Platforms**: Variable (1-8 tiles), creating chaotic layout
- **Gaps**: Large (3-7 tiles), demanding precise jumps
- **Floating Platforms**: Many (77% chance), creating vertical challenges
- **Decorations**: Minimal grass (45% coverage), sparse trees (9% chance)
- **Collectibles**: Few (15% chance), making rewards precious
- **Sky**: Red-to-dark-red gradient
- **Music**: Intense, driving background track

### Neutral Levels 
- **Atmosphere**: Peaceful clearing under calm azure sky
- **Platforms**: Balanced (4-10 tiles), standard platforming
- **Gaps**: Moderate (2-4 tiles), fair challenges
- **Floating Platforms**: Some (40% chance), varied gameplay
- **Decorations**: Good coverage (85% grass, 15% trees)
- **Collectibles**: Moderate (30% chance), balanced rewards
- **Sky**: Standard blue gradient
- **Music**: Calm, ambient background track

## 🔧 Technical Implementation

### AI Prompt Engineering
The system uses carefully crafted prompts to ensure consistent, high-quality AI responses:

```python
# Emotion Classification
"Analyze the emotional tone and respond with EXACTLY ONE WORD from: joy, fear, anger, or neutral"

# Narrative Generation  
"Create a concise, immersive 10-second game intro narrative that blends the user's real experience with the fox's adventure"
```

### Level Data Format
Levels are stored as CSV files with separate layers:
- `terrain.csv` - Solid platforms and ground tiles
- `coins.csv` - Collectible item positions
- `grass.csv` - Decorative vegetation
- `fg_palms.csv` - Foreground palm trees
- `bg_palms.csv` - Background palm trees  
- `player.csv` - Spawn point and goal location


## Audio Design

### Background Music System
Each emotion has a dedicated background track:
- **Joy**: `bgm_joy.wav` - Uplifting, energetic melody
- **Fear**: `bgm_fear.wav` - Tense, atmospheric soundscape  
- **Anger**: `bgm_anger.wav` - Intense, driving rhythm
- **Neutral**: `bgm_neutral.wav` - Calm, ambient tones

### Sound Effects
- **Jump**: Satisfying hop sound with emotion-based volume
- **Coin Collection**: Rewarding chime when collecting items
- **Death**: Dramatic sound when falling off the level
- **Victory**: Triumphant fanfare when completing the level

### Text-to-Speech Narration
- **Edge-TTS Integration**: Microsoft's high-quality neural voices
- **Emotion-Specific Voices**: Different voices for different emotions
- **Background Generation**: Speech generated asynchronously
- **Skip Controls**: Players can skip or stop narration


## Development & Customization

### Adding New Emotions
1. Update `MOOD_ATMOSPHERES` in `prompts.py`
2. Add emotion parameters in `level_generator.py`
3. Create corresponding sky background in `graphics/decoration/sky/`
4. Add background music track in `audio/bgm/`
5. Update player physics in `player.py`

### Modifying Level Generation
Adjust parameters in `level_generator.py`:
```python
# Example: Make joy levels even more generous
if emotion == 'joy':
    self.coin_chance = 0.8  # Increase from 0.6
    self.platform_min_length = 8  # Increase from 6
```

### Custom AI Prompts
Modify prompts in `prompts.py` to change AI behavior:
- Adjust `EMOTION_EXTRACTION_PROMPT` for different emotion classification
- Modify `NARRATIVE_GENERATION_PROMPT` for different story styles

## Troubleshooting

### Common Issues

**Game won't start**
- Ensure Python 3.10 is installed
- Check all dependencies are installed: `pip install -r requirements.txt`
- Verify graphics files exist in `graphics/` directory

**AI not working**
- Check OpenAI API key is valid and has credits
- Verify internet connection for API calls
- Check console for error messages

**No sound**
- Ensure audio files exist in `audio/` directory
- Check system audio settings
- Verify pygame audio initialization



### Development Setup
```bash


# Create virtual environment
conda create --name myenv python=3.10 
conda activate myenv  

# Install development dependencies
pip install -r requirements.txt


```





