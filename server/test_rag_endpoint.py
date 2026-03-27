#!/usr/bin/env python3
"""
Test RAG endpoint with proper error handling and streaming response parsing
"""

import requests
import json
import sys

def test_rag_endpoint():
    """Test the /diagnosis/rag endpoint"""
    
    url = "http://localhost:8000/diagnosis/rag"
    
    patient_data = {
        "text": "35-year-old female, extreme fatigue and brain fog for 2 months, numbness in hands/feet, vegetarian, takes metformin"
    }
    
    print("=" * 70)
    print("TESTING RAG ENDPOINT")
    print("=" * 70)
    print(f"\nEndpoint: POST {url}")
    print(f"Patient: {patient_data['text']}\n")
    
    try:
        print("🔄 Sending request...")
        response = requests.post(
            url,
            json=patient_data,
            headers={"Content-Type": "application/json"},
            timeout=30,
            stream=True
        )
        
        print(f"✓ Response Status: {response.status_code}")
        print(f"✓ Content-Type: {response.headers.get('Content-Type', 'N/A')}")
        
        if response.status_code == 200:
            print("\n📊 STREAMING RESPONSE:")
            print("-" * 70)
            
            # Handle Server-Sent Events streaming response
            full_response = ""
            for chunk in response.iter_lines(decode_unicode=True):
                if chunk:
                    full_response += chunk + "\n"
                    # Parse SSE events
                    if chunk.startswith("data: "):
                        try:
                            event_data = json.loads(chunk[6:])
                            if event_data.get("type") == "token":
                                print(event_data.get("content", ""), end="", flush=True)
                            elif event_data.get("type") == "citations":
                                print("\n\n📚 CITATIONS:")
                                for citation in event_data.get("data", [])[:3]:
                                    print(f"  • {citation.get('micronutrient')} ({citation.get('category')})")
                        except json.JSONDecodeError:
                            pass
            
            print("\n" + "-" * 70)
            print("✅ RAG endpoint working correctly!")
            return True
        else:
            print(f"\n❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server at http://localhost:8000")
        print("   Make sure the API server is running: python streaming_api.py")
        return False
    except requests.exceptions.Timeout:
        print("❌ Request timed out (>30 seconds)")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_rag_status():
    """Test the /rag/status endpoint"""
    
    url = "http://localhost:8000/rag/status"
    
    print("\n" + "=" * 70)
    print("TESTING RAG STATUS ENDPOINT")
    print("=" * 70)
    print(f"\nEndpoint: GET {url}\n")
    
    try:
        print("🔄 Sending request...")
        response = requests.get(url, timeout=10)
        
        print(f"✓ Response Status: {response.status_code}\n")
        
        if response.status_code == 200:
            data = response.json()
            print("📋 RAG SYSTEM STATUS:")
            for key, value in data.items():
                print(f"  • {key}: {value}")
            print("\n✅ RAG status endpoint working!")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    print("\n🚀 VITACHECK RAG ENDPOINT TESTS\n")
    
    # Test status first
    status_ok = test_rag_status()
    
    if status_ok:
        # Test diagnosis endpoint
        diagnosis_ok = test_rag_endpoint()
        
        if diagnosis_ok:
            print("\n" + "=" * 70)
            print("✅ ALL TESTS PASSED - RAG System is operational!")
            print("=" * 70)
            sys.exit(0)
    
    sys.exit(1)
