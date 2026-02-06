### To run the AI
dramatiq tasks

### To run the backend main.py server
uvicorn main:app --reload --port 8000

### Start the Redis service (ubuntu powershell)
sudo service redis-server start

### Verify it is working (it should return "PONG") (ubuntu powershell)
redis-cli ping



### Installing Ollama model (powershell)
ollama run deepseek-r1:8b
### Run the Ollama model
ollama serve

### Installing Ollama client in /server
pip install ollama





pip install uvicorn fastapi ollama dramatiq[redis] redis pydantic