# Quick Start: Testing VitaCheck Phase 1

## TL;DR - Everything works, here's what to expect

### Current Status
- ✅ Backend (port 8000) running
- ✅ Frontend (port 5173) running  
- ✅ System fully operational

### Expected Performance
- **First result**: 14-15 seconds
- **Full result**: 45-60 seconds
- **Why**: DeepSeek's reasoning takes ~13s before outputting anything

---

## Quick Test (Choose One)

### Test A: Via Web UI (Recommended)
```
1. Visit: http://localhost:5173
2. Fill out the 7 symptom categories (rate 0-4)
3. Add optional narrative: "I've been feeling this way for 2 weeks"
4. Click "Start AI Analysis"
5. WAIT 14 seconds... (you'll see "Analyzing Symptoms")
6. Watch diagnosis stream in real-time
7. See results in ~50 seconds total
```

### Test B: Via cURL (Fast)
```bash
curl -X POST http://localhost:8000/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"text": "I feel tired and weak"}' \
  -w "\nTotal time: %{time_total}s\n"

# You'll see SSE events:
# data: {"type": "status", ...}
# data: {"type": "token", "content": "...clinical text..."}
# Completes in ~49-50 seconds
```

### Test C: Check Health
```bash
curl http://localhost:8000/health
# Response: {"status": "healthy", "ollama": "running", "groq": "configured"}
```

---

## Understanding the Timeline

### The 49-Second Response Explained
```
Time  | What's Happening
------|----------------------------------
0s    | Client sends symptom data
0.2s  | Groq extracts symptoms (fast)
0.5s  | RAG context retrieved  
0.5s  | DeepSeek starts thinking
13s   | ⭐ FIRST OUTPUT TOKEN APPEARS (TTFT)
      | (This is what you wait for)
49s   | Full diagnosis complete
```

### Why Does It Feel Like Nothing is Happening?
- Seconds 0-13: System is thinking (internally reasoning)
- You'll see status: "Analyzing Symptoms"
- UI shows: TTFT: 13942ms ⚡
- Then: Diagnosis streams in real-time ✨

---

## Troubleshooting

### "Port 8000 connection refused"
```powershell
# Check if server is running
netstat -ano | findstr :8000

# If yes, give it a moment (startup can take 5-10s)
# If no, restart server:
cd server
python streaming_api.py
```

### "Takes 2+ minutes"
- **Cause**: Ollama model not loaded, or running out of memory
- **Fix**: 
  ```bash
  ollama pull deepseek-r1:8b
  ollama serve  # Restart
  ```

### "No response at all"
- Check Ollama is running: `curl http://localhost:11434/api/tags`
- Check frontend reached: `curl http://localhost:8000/docs`
- Check .env has `GROQ_API_KEY` (should be there already)

### "Response looks weird or cuts off"
- This is probably thinking blocks being displayed
- Check PERFORMANCE_ANALYSIS.md for details
- Or see `/docs` at http://localhost:8000

---

## What to Look For (Quality Checks)

### ✅ Good Response
```json
{
  "type": "status",
  "message": "Extracting symptoms..."
}
{
  "type": "extracted",
  "data": {
    "symptoms": ["your symptoms here"],
    "age": 0,
    "sex": "unknown"
  }
}
{
  "type": "token",
  "content": "## 1) Symptoms Analysis\n\n* **Tiredness**..."
}
```
- Status messages appear immediately ✅
- Extraction shows your symptoms ✅
- Tokens arrive progressively ✅
- Final diagnostic text is coherent ✅

### ❌ If Something's Wrong
- No "status" messages → Check backend running
- Empty "extracted" data → Check Groq API
- Tokens only appear at end → Check streaming headers
- Very slow extraction → Groq API slower than expected

---

## Key Documentation

| Document | Use This If |
|----------|-----------|
| USAGE_GUIDE.md | Want complete setup instructions |
| PERFORMANCE_ANALYSIS.md | Want to understand the latency |
| FIXES_APPLIED.md | Want to see what was changed |
| ACTIVE_VS_DEPRECATED.md | Want to understand file structure |

---

## The Bottom Line

**Everything is working correctly.**

- The 49-second response time ≠ bug
- It's the model taking time to reason
- This is normal for reasoning models
- First indicator of activity within 1 second
- First actual output within 14 seconds
- Full diagnosis by 50 seconds

**Choose your preference:**
1. Keep it (best reasoning, slower)
2. Switch to Mixtral (fast extraction, less reasoning)
3. Both (hybrid approach - Phase 2)

---

## Next Steps

1. **Test the UI** (recommended first)
   - http://localhost:5173
   - Go through questionnaire
   - Watch it work

2. **Review the docs**
   - PERFORMANCE_ANALYSIS.md (why latency?)
   - USAGE_GUIDE.md (all details)

3. **Plan Phase 2**
   - Model optimization?
   - Hybrid approach?
   - QLoRA fine-tuning?

4. **Questions?**
   - Check `/docs` at http://localhost:8000
   - Review streaming_api.py (well-commented)
   - See client hook: useStreamingDiagnosis.ts

---

## Common Questions

**Q: Why is it so slow?**  
A: DeepSeek is a reasoning model. It thinks before it talks. This takes time. See PERFORMANCE_ANALYSIS.md.

**Q: Is it actually streaming?**  
A: Yes! Check the SSE events. First token usually appears ~13 seconds in, then streams continuously.

**Q: Can I make it faster?**  
A: Yes - switch to Mixtral (5-10s, less reasoning) or use GPT-4 (3-5s, costs money). See Phase 2 plans.

**Q: Is my input being used?**  
A: Yes! Check the SSE stream - you'll see your symptoms extracted and analyzed.

**Q: Do I need Groq API?**  
A: No, it's optional. System works without it (slower extraction). But it's configured and working now.

---

**Status: ✅ Ready to test**  
**Location: http://localhost:5173**  
**Expected wait**: 14s to first output, 50s total  
**Confidence level**: High - all systems verified working
