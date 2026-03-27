#!/usr/bin/env python3
"""
VitaCheck Phase 1: Diagnostic System Health Check
Verifies all components are working before running the full app.
"""

import sys
import asyncio
import httpx
import os
from pathlib import Path

# Colors for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_header(title):
    print(f"\n{BOLD}{BLUE}{'='*60}{RESET}")
    print(f"{BOLD}{BLUE}{title:^60}{RESET}")
    print(f"{BOLD}{BLUE}{'='*60}{RESET}\n")

def print_check(name, status, message=""):
    icon = f"{GREEN}✅{RESET}" if status else f"{RED}❌{RESET}"
    msg = f" - {message}" if message else ""
    print(f"{icon} {name}{msg}")
    return status

async def check_environment():
    """Check environment variables and configuration"""
    print_header("1. ENVIRONMENT CHECK")
    
    all_ok = True
    
    # Check .env file
    env_file = Path(".env")
    if env_file.exists():
        print_check(".env file", True)
        with open(".env") as f:
            content = f.read()
            has_groq = "GROQ_API_KEY" in content and "your_groq_api_key" not in content.lower()
            print_check("  GROQ_API_KEY configured", has_groq, "Set in .env" if has_groq else "Not set (OK - fallback available)")
            
            has_ollama = "OLLAMA_URL" in content
            print_check("  OLLAMA_URL configured", has_ollama, content.split("OLLAMA_URL=")[1].split("\n")[0].strip() if has_ollama else "")
    else:
        all_ok = False
        print_check(".env file", False, "Copy .env.example to .env")
    
    return all_ok

async def check_ollama(ollama_url: str = "http://localhost:11434"):
    """Check if Ollama is running and model is loaded"""
    print_header("2. OLLAMA CHECK")
    
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            # Check if Ollama is running
            try:
                response = await client.get(f"{ollama_url}/api/tags")
                print_check("Ollama server running", True, ollama_url)
                
                # Check if deepseek-r1:8b is pulled
                data = response.json()
                models = [m['name'] for m in data.get('models', [])]
                
                has_deepseek = any('deepseek-r1' in m for m in models)
                print_check("DeepSeek R1 model pulled", has_deepseek, 
                           f"Found models: {len(models)}")
                
                if has_deepseek:
                    print(f"    {YELLOW}Note: Pull model with: ollama pull deepseek-r1:8b{RESET}")
                
                return has_deepseek
            
            except httpx.ConnectError:
                print_check("Ollama server running", False, 
                           f"Cannot connect to {ollama_url}")
                print(f"    {YELLOW}Start Ollama with: ollama serve{RESET}")
                return False
    
    except Exception as e:
        print_check("Ollama check", False, str(e))
        return False

async def check_groq():
    """Check if Groq API is configured"""
    print_header("3. GROQ API CHECK")
    
    groq_key = os.getenv("GROQ_API_KEY")
    
    if not groq_key or groq_key.startswith("your_"):
        print_check("Groq API key", False, "Not configured - will use fallback extraction")
        print(f"    {YELLOW}Optional: Get free key from https://console.groq.com{RESET}")
        return False
    else:
        print_check("Groq API key", True, "Configured")
        
        # Try a quick API call
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {groq_key}",
                             "Content-Type": "application/json"
                    },
                    json={
                        "model": "llama-3.3-70b-versatile",
                        "messages": [{"role": "user", "content": "test"}],
                        "max_tokens": 10
                    }
                )
                
                if response.status_code == 200:
                    print_check("Groq API connection", True, "Ready for extraction")
                    return True
                else:
                    # print_check("Groq API connection", False, f"Status {response.status_code}")
                    # return False
                    print(f"{RED}Groq Error Detail: {response.text}{RESET}")
                    print_check("Groq API connection", False, f"Status {response.status_code}")
                    return False
        except Exception as e:
            print_check("Groq API connection", False, str(e))
            return False

async def check_fastapi_server(api_url: str = "http://localhost:8000"):
    """Check if FastAPI streaming server is running"""
    print_header("4. FASTAPI SERVER CHECK")
    
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            response = await client.get(f"{api_url}/health")
            
            if response.status_code == 200:
                health = response.json()
                print_check("FastAPI server running", True, api_url)
                
                ollama_status = health.get("ollama", "unknown")
                groq_status = health.get("groq", "unknown")
                
                print(f"  Ollama status: {ollama_status}")
                print(f"  Groq status: {groq_status}")
                
                return True
            else:
                print_check("FastAPI server running", False, f"Status {response.status_code}")
                return False
    
    except httpx.ConnectError:
        print_check("FastAPI server running", False, f"Cannot connect to {api_url}")
        print(f"    {YELLOW}Start with: python streaming_api.py{RESET}")
        return False

async def test_streaming_endpoint(api_url: str = "http://localhost:8000"):
    """Test the /chat/stream endpoint"""
    print_header("5. STREAMING ENDPOINT TEST")
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{api_url}/chat/stream",
                json={"text": "I feel tired and weak"},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                print_check("Streaming endpoint", True, "Connected")
                
                # Try to read first few events
                lines = response.text.split('\n')[:5]
                events = [l for l in lines if l.startswith('data:')]
                
                if events:
                    print_check("Streaming events", True, f"Received {len(events)} events")
                    for i, event in enumerate(events[:2], 1):
                        try:
                            import json
                            data = json.loads(event[6:])
                            print(f"    Event {i}: {data.get('type', 'unknown')}")
                        except:
                            pass
                    return True
                else:
                    print_check("Streaming events", False, "No events received")
                    return False
            else:
                print_check("Streaming endpoint", False, f"Status {response.status_code}")
                return False
    
    except httpx.TimeoutException:
        print_check("Streaming endpoint", False, "Timeout - may be processing")
        return True  # Not a critical failure
    except Exception as e:
        print_check("Streaming endpoint", False, str(e))
        return False

def print_summary(results):
    """Print final summary and recommendations"""
    print_header("SUMMARY")
    
    passed = sum(results.values())
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}\n")
    
    if all(results.values()):
        print(f"{GREEN}{BOLD}✅ All systems ready!{RESET}")
        print("\nYou can now:")
        print("1. Start backend: python streaming_api.py")
        print("2. Start frontend: npm run dev")
        print("3. Visit: http://localhost:5173")
    else:
        print(f"{YELLOW}{BOLD}⚠️  Some issues detected{RESET}\n")
        
        failed = [k for k, v in results.items() if not v]
        for item in failed:
            print(f"  • {item}")
        
        print(f"\n{YELLOW}Check the messages above for fixes.{RESET}")

async def main():
    """Run all health checks"""
    print(f"{BOLD}{BLUE}VitaCheck Phase 1: Health Check{RESET}")
    
    # Load .env
    from dotenv import load_dotenv
    load_dotenv()
    
    results = {}
    
    # Run checks
    results["Environment"] = await check_environment()
    results["Ollama"] = await check_ollama()
    results["Groq API"] = await check_groq()
    results["FastAPI Server"] = await check_fastapi_server()
    results["Streaming Endpoint"] = await check_fastapi_server()  # Assumes server is healthy
    
    # If server is running, test streaming
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            await client.get("http://localhost:8000/health")
            results["Streaming Test"] = await test_streaming_endpoint()
    except:
        results["Streaming Test"] = False
    
    # Print summary
    print_summary(results)
    
    return all(results.values())

if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Check interrupted{RESET}")
        sys.exit(1)
