import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import pickle

# 1. โหลดข้อมูลจากไฟล์ Excel
df = pd.read_excel('training_data.xlsx')

# 2. ชื่อคอลัมน์ที่ปรับให้ตรงกับในไฟล์ Excel แล้ว
features = ['daily_work_hours', 'break_frequency_hr', 'ergonomic_chair', 
            'exercise_days_per_wk', 'posture_score', 'stress_level', 'pain_score_neck_back']

X = df[features]
y = df['risk_level']  # เปลี่ยนชื่อคอลัมน์ตรงนี้

# 3. สร้างและฝึกสอนโมเดล Decision Tree 
model = DecisionTreeClassifier(max_depth=5, random_state=42)
model.fit(X, y)

# 4. บันทึกโมเดลเป็นไฟล์ .pkl
with open('model.pkl', 'wb') as file:
    pickle.dump(model, file)

print("สร้างไฟล์ model.pkl สำเร็จ!")