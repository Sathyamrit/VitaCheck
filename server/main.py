from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import PatientData, ReportStatus
import tasks
import redis

# Use decode_responses=True to handle strings instead of bytes
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Pre-load medical diagnostic models into memory here
    print("VitaCheck AI Gateway Online...")
    yield
    redis_client.close()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

@app.post("/generate-report/{user_id}", response_model=ReportStatus)
async def create_report(user_id: str, data: PatientData):
    try:
        task = tasks.generate_ai_diagnosis.send(user_id, data.model_dump())
        redis_client.set(f"status:{task.message_id}", "processing")
        return {"task_id": task.message_id, "status": "processing"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/report-status/{task_id}")
async def get_status(task_id: str):
    status = redis_client.get(f"status:{task_id}")
    result = redis_client.get(f"result:{task_id}")
    return {
        "status": status if status else "not_found",
        "data": result if result else None
    }

@app.post("/generate-meal-plan")
async def start_meal_generation(data: dict):
    # Triggers the new recipe actor
    task = tasks.generate_meal_plan.send(data['diagnosis'], data['preferences'])
    redis_client.set(f"recipes_status:{task.message_id}", "processing")
    return {"recipe_task_id": task.message_id}

@app.get("/recipe-status/{task_id}")
async def get_recipe_status(task_id: str):
    status = redis_client.get(f"recipes_status:{task_id}")
    data = redis_client.get(f"recipes_result:{task_id}")
    return {"status": status, "data": data}