from fastapi import FastAPI
from firebase_admin import credentials, firestore, initialize_app

app = FastAPI()

cred = credentials.Certificate("serviceAccountKey.json")
initialize_app(cred)
db = firestore.client()

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
    import uvicorn

