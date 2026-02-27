from fastapi import FastAPI
from google.oauth2 import service_account
from google.cloud import firestore
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # لاحقًا نقدر نخصصه لرابط الواجهة فقط
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# إعداد بيانات الاعتماد
credentials = service_account.Credentials.from_service_account_info({
    "type": "service_account",
    "project_id": os.getenv("FIREBASE_PROJECT_ID"),
    "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
    "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace("\\n", "\n"),
    "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
    "client_id": os.getenv("FIREBASE_CLIENT_ID"),
    "auth_uri": os.getenv("FIREBASE_AUTH_URI"),
    "token_uri": os.getenv("FIREBASE_TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_X509_CERT_URL"),
})

db = firestore.Client(
    project=os.getenv("FIREBASE_PROJECT_ID"),
    credentials=credentials
)

@app.get("/")
def root():
    return {"message": "Talent AI Backend is running"}

@app.get("/schools")
def get_schools():
    docs = db.collection("schools").stream()
    return [d.to_dict() for d in docs]

@app.get("/students")
def get_students():
    docs = db.collection("students").stream()
    return [d.to_dict() for d in docs]

@app.get("/grades/{student_id}")
def get_grades(student_id: str):
    docs = db.collection("grades").where("student_id", "==", student_id).stream()
    return [d.to_dict() for d in docs]

@app.get("/activities/{student_id}")
def get_activities(student_id: str):
    docs = db.collection("activities").where("student_id", "==", student_id).stream()
    return [d.to_dict() for d in docs]

@app.get("/analyze/{student_id}")
def analyze_student(student_id: str):
    grades_ref = db.collection("grades").where("student_id", "==", student_id).stream()
    grades = [g.to_dict() for g in grades_ref]

    if not grades:
        return {"error": "No grades found"}

    avg_math = sum(g["math_score"] for g in grades) / len(grades)
    avg_science = sum(g["science_score"] for g in grades) / len(grades)
    avg_language = sum(g["language_score"] for g in grades) / len(grades)
    avg_creativity = sum(g["creativity_score"] for g in grades) / len(grades)

    talent_index = round((avg_math + avg_science + avg_language + avg_creativity) / 4, 2)

    return {
        "student_id": student_id,
        "talent_index": talent_index,
        "details": {
            "math": avg_math,
            "science": avg_science,
            "language": avg_language,
            "creativity": avg_creativity
        }
    }
