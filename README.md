# VitaCheck

An AI-powered health platform for micronutrient deficiency diagnosis, meal planning, and personalized nutrition recommendations.

## Overview

VitaCheck is a comprehensive health technology platform that leverages advanced AI models to help users understand their nutritional health. By analyzing symptoms and providing evidence-based recommendations, VitaCheck aims to address the global issue of micronutrient deficiencies.

## Features

### 🔍 Symptom-Based Diagnosis
- AI-powered analysis of user-reported symptoms
- Identifies potential vitamin and mineral deficiencies
- Provides detailed explanations with medical evidence

### 🍽️ Personalized Meal Planning
- Generates recipes tailored to address specific nutritional gaps
- Integrates USDA food composition data
- Considers drug-nutrient interactions for safety

### 📊 RAG-Enhanced Responses
- Retrieval Augmented Generation for accurate nutrition information
- Knowledge base built from medical and scientific sources
- Real-time streaming responses for interactive experience

### 🔒 Safety Guardrails
- Drug-nutrient interaction checking
- Evidence-based recommendations only
- User preference management

## Tech Stack

### Frontend
- **React** with TypeScript
- **Vite** for fast development
- **CSS** for styling

### Backend
- **Python** with FastAPI
- **DeepSeek R1 8B** for AI reasoning
- **ChromaDB** for vector storage
- **RAG pipeline** for knowledge retrieval

### Infrastructure
- **Groq** for fast inference
- **Ollama** for local model deployment
- **Server-Sent Events (SSE)** for streaming responses

## Project Structure

```
VitaCheck/
├── client/                 # React frontend
│   ├── src/
│   │   ├── components/    # UI components
│   │   ├── hooks/         # Custom React hooks
│   │   ├── pages/         # Page components
│   │   ├── types/         # TypeScript types
│   │   └── utils/         # Utility functions
│   └── package.json
│
├── server/                # Python backend
│   ├── safety/           # Guardrails & safety checks
│   ├── evaluation/       # Benchmarking & metrics
│   ├── Knowledge Base/   # Nutrition datasets
│   └── chroma_db/        # Vector database
│
├── docs/                 # Implementation documentation
└── health_check.py       # Main health check script
```

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.10+
- Groq API key (free at https://console.groq.com)
- Ollama (optional, for local inference)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Sathyamrit/VitaCheck.git
   cd VitaCheck
   ```

2. **Set up the backend**
   ```bash
   cd server
   pip install -r requirements.txt
   # Create .env file with GROQ_API_KEY=your_api_key
   ```

3. **Set up the frontend**
   ```bash
   cd client
   npm install
   ```

### Running the Application

1. **Start the backend server**
   ```bash
   cd server
   python streaming_api.py
   ```

2. **Start the frontend**
   ```bash
   cd client
   npm run dev
   ```

3. Open http://localhost:5173 in your browser

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/chat/stream` | POST | Streaming AI diagnosis |
| `/rag/query` | POST | RAG-based nutrition queries |
| `/user/preferences` | GET/POST | User profile management |
| `/safety/check` | POST | Drug-nutrient interaction check |

## Documentation

Detailed implementation guides are available in the `docs/` folder:

- [Phase 1: Streaming API Foundation](docs/PHASE1_COMPLETE.md)
- [Phase 2: Model Infrastructure](docs/PHASE2_COMPLETION.md)
- [Phase 3: RAG Pipeline](docs/PHASE3_IMPLEMENTATION.md)
- [Phase 4: Fine-tuning](docs/PHASE4_IMPLEMENTATION.md)
- [Phase 5: Safety Evaluation](docs/PHASE5_SAFETY_EVALUATION.md)
- [Phase 6: Production Deployment](docs/PHASE6_PRODUCTION_DEPLOYMENT.md)

## License

MIT License

## Disclaimer

This platform is for informational purposes only and does not constitute medical advice. Always consult with a healthcare professional for medical concerns.