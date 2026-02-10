# Fitness Tracker App

Monorepo containing:
- React Native (Expo) mobile app
- Python (FastAPI) backend for fitness plans, meals, and workouts

## Structure
- fitness-coach-app/ → mobile app
- fitness-backend/ → API & business logic
---

## Tech Stack

### Frontend
- React Native
- Expo
- TypeScript
- Expo Router

### Backend
- Python
- FastAPI
- SQLAlchemy
- Alembic (migrations)
- PostgreSQL / SQLite (local development)

---

## Prerequisites

- Node.js (LTS)
- npm
- Python 3.10+
- (Optional for iOS) Xcode + CocoaPods
- (Optional for Android) Android Studio

---

## Backend Setup
Run the following commands from the project root:
```bash
cd fitness-backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```
The backend API will be available at:
http://127.0.0.1:8000

## Frontend Setup
Open a new terminal and run:
```bash
cd fitness-coach-app
npm install
npx expo start
```

You can run the app using:
- Expo Go (scan the QR code)
- iOS Simulator
- Android Emulator

---
## Common Issues
If the mobile app cannot reach the backend:

- Ensure the backend server is running
- Use your machine’s LAN IP instead of localhost
- Confirm your phone and computer are on the same Wi-Fi network







