# Blackjack (Python + CustomTkinter)

A simple Blackjack game with a GUI built using **CustomTkinter**.

---

## Features

* Standard Blackjack rules (Hit / Stand)
* Betting system with balance tracking

---

## Project Structure

```
blackjack-gui/
│
├── engine.py            # Game logic (deck, hands, rules)
├── gui.py               # Main GUI application
├── card_manager.py      # Loads and manages card images
├── process_images.py    # used to crop and resize raw images. Not necessary running gui. It requires a "Cards (large)/" directory having raw images to run without crashing.
│
├── cards_cropped_resized/   # Final card assets used in UI
├── Cards (large)/          # (not included here) raw images downloaded from kenney.nl
│
└── .gitignore
```

---

## How It Works

### Game Engine

* Handles:

  * deck creation & shuffling
  * dealing cards
  * player/dealer actions
  * hand value calculation
  * betting & balance

### GUI

* Displays:

  * player & dealer cards
  * current balance
  * game state (betting / playing / result)
* Updates based on engine state

### Card Manager

* Loads images once at startup
* Maps `(rank, suit)` → image
* Handles special cards (back, empty, etc.)

---

## Installation

### 1. Clone repo

```
git clone https://github.com/ks-kishan/blackjack-gui.git
cd blackjack-gui
```

### 2. Install dependencies

```
pip install customtkinter pillow
```

---

## Run

```
python gui.py
```

---

## Notes

* image assets are downloaded from kenney.nl's playing cards deck
* Original assets are not included here and only cropped and resized version of them is included here.
* process_images.py file is not necessary for running the game.

---

## Limitations

* No advanced Blackjack features:

  * no split
  * no double down
* No animations
* Fixed window size

---

## Future Improvements

* Card animations (deal, flip)
* Better layout (card overlap like real table)
* Support for split / double down
* Sound effects
* Responsive UI

---

## Why This Project

Built to:

* practice GUI development with Tkinter/CustomTkinter
* understand separation of concerns (engine vs UI)

---

## Author

Kishan
