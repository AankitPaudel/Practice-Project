# File: README.md
# Virtual Teacher

An AI-powered teaching assistant that provides interactive learning experiences through voice and text interactions.

## Features

- Voice and text-based interactions
- Real-time speech-to-text and text-to-speech conversion
- RAG (Retrieval-Augmented Generation) for accurate responses
- Built on professor's lecture content
- Interactive chat interface

## Tech Stack

### Backend
- FastAPI
- SQLAlchemy
- LangChain
- ChromaDB
- OpenAI
- Whisper
- gTTS

### Frontend
- React
- Vite
- WebSocket

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/virtual-teacher.git
cd virtual-teacher
```

2. Create and set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configurations
```

3. Run with Docker:
```bash
docker-compose up --build
```

Or run locally:

Backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend:
```bash
cd frontend
npm install
npm run dev
```

## Development

### Adding New Lectures
1. Place lecture text files in `data/lectures/`
2. Use the API endpoint `/api/lectures/` to process them
3. The system will automatically index them for RAG

### API Documentation
- API docs available at `http://localhost:8000/docs`
- Swagger UI at `http://localhost:8000/redoc`

## Testing
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License
MIT