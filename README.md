# AI Emotion-Based Platformer Game

A 2D platformer that uses artificial intelligence to analyze your real-life experiences and dynamically generate personalized game levels based on your emotional state. Enter what you're feeling, and the game procedurally generates a new level with custom narrative audio.

## Installation

### Prerequisites
- Python 3.10
- OpenAI API key

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/sidhantgumber/AI-Emotion-Driven-Platformer.git
   cd FinalProject
   ```

2. **Create conda environment**
   ```bash
   conda create --name emotion-game python=3.10 
   conda activate emotion-game
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up OpenAI API key**
   
   Get your API key from [OpenAI](https://platform.openai.com/api-keys)
   
   **Option A: Environment Variable**
   ```bash
   # Windows
   setx OPENAI_API_KEY "your_api_key_here"
   
   # macOS/Linux
   export OPENAI_API_KEY="your_api_key_here"
   ```
   
   **Option B: Direct in code**
   Edit `scripts/ml_agents.py` line 17 and add your API key to the EmotionBrain() constructor

5. **Run the game**
   ```bash
   cd scripts
   python game.py
   ```

## How to Play

### Objective
Collect 5 coins and reach the pirate hat to win.

### Controls
- **WASD/Arrow Keys**: Move and jump
- **SPACE/W/UP**: Jump
- **R**: New experience (restart or return to input)
- **S**: Skip/stop narration
- **ESC**: Quit game

### Gameplay Flow
1. Enter a description of your day or feelings in the text box
2. AI analyzes your emotion and generates a custom level
3. Listen to the personalized narrative (optional)
4. Navigate the level that reflects your emotional state
5. Collect coins and reach the goal to win

## Emotion System

The AI analyzes your input and classifies it into four core emotions:

| Emotion | Examples | Level Characteristics |
|---------|----------|----------------------|
| **Joy** | "Got promoted!", "Beautiful sunset", "Had a great date" | Bouncy physics, long platforms, abundant collectibles |
| **Fear** | "Job interview tomorrow", "Heard strange noises", "Feeling anxious" | Heavy physics, short platforms, sparse rewards |
| **Anger** | "Traffic jam!", "Unfair treatment", "Broken promises" | Aggressive physics, chaotic layout, challenging jumps |
| **Neutral** | "Normal day", "Drank water", "Watched TV" | Balanced physics, standard platforming |

### Physics Adaptation
Your character's movement changes based on detected emotion:

- **Joy**: Light gravity (0.4), fast speed (6), high jumps (-16)
- **Fear**: Heavy gravity (1.3), slow speed (4), powerful jumps (-20)
- **Anger**: Heavy gravity (1.3), very fast speed (9), explosive jumps (-28)
- **Neutral**: Balanced gravity (0.9), moderate speed (5), standard jumps (-20)

## Troubleshooting

**Game won't start**
- Ensure Python 3.10 is installed
- Check dependencies: `pip install -r requirements.txt`
- Verify graphics files exist in `graphics/` directory

**AI not working**
- Check OpenAI API key is valid and has credits
- Verify internet connection
- Restart terminal after setting environment variable

**No sound**
- Ensure audio files exist in `audio/` directory
- Check system audio settings

## Technical Details

### Core Components
- **ml_agents.py**: OpenAI integration for emotion detection and narrative generation
- **level_generator.py**: Procedural level generation based on emotions
- **player.py**: Emotion-adaptive physics and controls
- **level_viewer.py**: Game state management and rendering
- **tts.py**: Text-to-speech narration system
- **audio_manager.py**: Sound effects and background music

### Level Generation
Each emotion affects:
- Platform lengths and gap sizes
- Floating platform frequency
- Decoration density
- Collectible placement
- Sky background colors
- Background music selection
