### To run the AI
dramatiq tasks

### To run the backend main.py server
    # 1. Create a virtual environment named 'venv'
    python -m venv venv

    # 2. Activate it (this forces the terminal to see uvicorn)
    .\venv\Scripts\activate

    # 3. Install your requirements inside this bubble
    pip install uvicorn fastapi

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



Get-Process ollama* | Stop-Process -Force

pip install uvicorn fastapi ollama dramatiq[redis] redis pydantic



### nutritional values - marcros n all

### Lifestyle

### Height weight n all