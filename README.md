# Snake Game

Classic Snake game with acceleration mechanic, written in Python using Pygame.

## Features

- 🎮 Smooth controls using arrow keys
- ⚡ Acceleration when holding the key in the direction of movement
- 🍎 Apples give points and grow the snake
- 🥔 Rotten potatoes deduct points

## Requirements

- Python 3.8 or newer
- Pygame

## Installation & Running

### Running from source

1. Install Python 3.8 or newer
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Run the game:
```bash
python main.py
```

### Compiling to .exe

```bash
pip install pyinstaller
pyinstaller --onefile --noconsole --name "Snake Game" --hidden-import=pygame --icon=icon.ico snake_game.py
```

The compiled `.exe` file will be located in the `dist/` folder.

