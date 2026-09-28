# Monasteries

> A full-stack, real-time multiplayer adaptation of the classic abstract strategy board game **Cathedral** — built as a personal portfolio project to explore WebSocket communication, game engine design, and modern web development.

---

## What is this?

**Monasteries** is a browser-based, two-player strategy game inspired by [Cathedral](https://en.wikipedia.org/wiki/Cathedral_(board_game)) (1978, Robert Moore) — a game where two players compete to claim territory on a 10×10 grid by placing uniquely shaped medieval buildings. Whoever leaves their opponent with the least usable space wins.

The project started as a way to build something non-trivial end-to-end: a real game with real rules, real-time multiplayer, and a clean separation between the game engine, server logic, and frontend UI.

---

## Features

-  **Real-time multiplayer** over WebSocket (no refresh needed — moves appear instantly)
-  **Guest play** — jump in without creating an account
-  **Time controls** with Fischer increment
-  **Move history** panel
-  **Draw offers, resignation, and rematch** with automatic color swap
-  **Territory capture** — enclosed areas are detected via BFS and pieces are removed automatically

---

## Tech Stack

This project is intentionally split into a standalone game engine, a Python backend, and a React frontend — each with its own clear responsibility.

###  Game Engine (pure Python)
The engine has zero framework dependencies — it's just Python. This made it easy to test in isolation and reason about correctness before wiring it to a server.

- BFS-based territory detection and capture logic
- Piece rotation and placement validation
- Interior piece detection for removal after capture

###  Backend
| Library | Role |
|---|---|
| **Flask** | App factory, REST API |
| **Flask-SocketIO** | Real-time WebSocket events |
| **Flask-SQLAlchemy** | ORM and database models |
| **Flask-Login** | Session management |
| **Flask-Bcrypt** | Password hashing |
| **Flask-Migrate** | Schema migrations |
| **python-dotenv** | Loads configuration from `.env` |
| **SQLite** | Default database (swappable) |
| **simple-websocket** | WebSocket transport for the threaded Werkzeug server |

###  Frontend
| Library | Role |
|---|---|
| **React 18 + Vite** | UI framework and build tooling |
| **React Router** | Client-side routing |
| **Socket.IO client** | Real-time communication |
| **Axios** | HTTP requests |
| **React Markdown** | In-app tutorial rendering |

---

## Project Structure

```
Monasteries/
├── backend/
│   ├── api/          # REST blueprints (auth, lobbies)
│   ├── db/           # SQLAlchemy models and CRUD
│   ├── engine/       # Core game logic (Board, Engine) ← self-contained
│   ├── game/         # Game state and session management
│   ├── models/       # Dataclasses and enums
│   ├── socket/       # SocketIO event handlers
│   ├── app.py        # App factory (dev / prod mode)
│   ├── config.py
│   ├── extensions.py
│   └── instances.py
├── frontend/
│   └── src/
│       ├── components/   # Reusable UI components
│       ├── hooks/        # useAuth, useGame, useLobby
│       ├── pages/        # LobbyPage, GamePage, TutorialPage
│       ├── services/     # API client, socket singleton
│       └── utils/        # Piece rotation utilities
├── migrations/       # Database migration scripts (committed)
├── tests/
│   ├── test_engine.py
│   ├── test_board.py
│   └── test_piece_catalog.py
├── .env.example      # Template for your local .env
└── run.py            # Entry point (dev / LAN mode)
```

---

## Getting Started

### Prerequisites
- Python 3.12+
- Node.js 18+

### 1. Install dependencies

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate       # Linux / macOS
.venv\Scripts\activate          # Windows

# Backend
pip install -r requirements.txt

# Frontend
cd frontend && npm install && cd ..
```

### 2. Configure the environment

The backend reads its settings from a `.env` file in the **project root** (next to `run.py`). Start from the template:

```bash
cp .env.example .env            # Windows: copy .env.example .env
```

Then edit `.env`:

```
SECRET_KEY=paste-a-long-random-string-here
# DATABASE_URL=sqlite:///cathedral.db
# ALLOWED_ORIGINS=http://192.168.1.10:5000
```

Generate a secret key with:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Notes:
- `.env` is git-ignored — only `.env.example` is committed.
- The `flask db ...` commands read `.env` automatically as well.
- The **frontend needs no `.env`**: it talks to the server on its own origin (in dev, Vite proxies requests to port 5000; in LAN mode Flask serves the built frontend itself).

### 3. Create the database

```bash
flask --app backend.app db upgrade
```

Migration scripts are committed in `migrations/`, so this single command creates all tables. If you change a model:

```bash
flask --app backend.app db migrate -m "describe the change"
flask --app backend.app db upgrade
```

---

## Running

`run.py` has two modes:

| Mode | Command | Binds to | Frontend served by |
|---|---|---|---|
| **LAN** (default) | `python run.py` | `0.0.0.0:5000` | Flask (built `frontend/dist`) |
| **Development** | `python run.py --dev` | `127.0.0.1:5000` | Vite dev server (`:5173`) |

### Development (localhost)

```bash
# terminal 1 — backend
python run.py --dev

# terminal 2 — frontend
cd frontend
npm run dev
```

Open `http://localhost:5173`. In this mode the Flask debugger and verbose Socket.IO logs are on, and the server only accepts connections from your own machine. Auto-reload is off (it is unreliable with WebSockets) — restart the backend manually after changing Python code.

### LAN play

Build the frontend once (and again after every frontend change), then start the server:

```bash
cd frontend && npm run build && cd ..
python run.py
```

The console prints the address to share, e.g. `http://192.168.1.10:5000`. Everyone on the same network opens that URL — one port serves both the frontend and the WebSocket traffic. If friends cannot connect, allow inbound TCP on port 5000 in your firewall.

Set a real `SECRET_KEY` in `.env` for this mode; the server logs a warning when it is missing.

### Optional flag

`python run.py --debug` additionally opens the Tk debug visualizer next to the server (works with either mode).

---

## Tests

The engine has its own test suite — no Flask or database involved:

```bash
pytest tests/ -v
```

Tests cover piece rotation, BFS territory detection, placement validation, and end-game scoring. The engine was developed test-first, which made debugging capture logic significantly easier.

---

## Configuration

All settings are optional environment variables (set them in `.env`):

| Variable | Default | Description |
|---|---|---|
| `SECRET_KEY` | insecure built-in value | Signs session cookies — **set this for LAN play** |
| `DATABASE_URL` | `sqlite:///cathedral.db` | Database connection string |
| `ALLOWED_ORIGINS` | dev: Vite (`localhost:5173`), LAN: any | Comma-separated list of allowed origins for CORS and Socket.IO |

---

## What I learned

- Structuring a **WebSocket-based game loop** — separating engine state from network events, handling disconnects gracefully, and keeping the server as the single source of truth
- Writing a **BFS-based board solver** from scratch and making it fast enough not to block the event loop
- Designing a **clean Python API** for the game engine so it could be tested without any web framework involved
- Managing **React state for real-time UI** — syncing socket events with component state without race conditions

---

## Inspiration

Monasteries is a fan-made digital adaptation of **Cathedral** (1978, Robert Moore). The original game uses beautifully crafted wooden pieces representing medieval buildings — this project is a personal, non-commercial tribute to it.

---

*Personal project — not affiliated with or endorsed by the publishers of Cathedral.*
