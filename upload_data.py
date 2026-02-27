import pandas as pd
from firebase_admin import credentials, firestore, initialize_app

cred = credentials.Certificate("serviceAccountKey.json")
initialize_app(cred)
db = firestore.client()

def upload_csv(collection_name, file_path):
    print(f"🔄 جاري رفع ملف: {file_path} إلى مجموعة: {collection_name}")
    df = pd.read_csv(file_path)
    print(f"📦 عدد السجلات: {len(df)}")

    for _, row in df.iterrows():
        db.collection(collection_name).add(row.to_dict())

    print(f"✅ تم رفع {collection_name} بنجاح\n")

# رفع كل الملفات
upload_csv("schools", "data/schools.csv")
upload_csv("students", "data/students.csv")
upload_csv("grades", "data/grades.csv")
upload_csv("activities", "data/activities.csv")

print("🎉 تم رفع جميع البيانات بنجاح!")