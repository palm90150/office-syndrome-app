from flask import Flask, request, render_template
import pickle
import os  # เพิ่มบรรทัดนี้

app = Flask(__name__)

# --- แก้ไขส่วนการโหลดโมเดลตรงนี้ ---
# หาตำแหน่งโฟลเดอร์ปัจจุบันที่ไฟล์ app.py อยู่
current_dir = os.path.dirname(os.path.abspath(__file__))
# เชื่อมที่อยู่โฟลเดอร์เข้ากับชื่อไฟล์ model.pkl
model_path = os.path.join(current_dir, 'model.pkl')

# โหลดโมเดลโดยใช้ path ใหม่
with open(model_path, 'rb') as file:
    model = pickle.load(file)
# --------------------------------

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # รับค่าจากฟอร์มหน้าเว็บ
        features = [
            float(request.form['daily_work_hours']),
            float(request.form['break_frequency_hr']),
            int(request.form['ergonomic_chair']),
            int(request.form['exercise_days_per_wk']),
            int(request.form['posture_score']),
            int(request.form['stress_level']),
            int(request.form['pain_score_neck_back'])
        ]
        
        # ทำนายผล
        raw_prediction = model.predict([features])[0]
        prediction = str(raw_prediction).strip().capitalize()
        
        # กำหนดสีและคำแนะนำตามระดับความเสี่ยง
        if prediction == 'Low':
            risk_text = "ความเสี่ยงต่ำ (Low Risk)"
            color = "#4CAF50" 
            bg_color = "#E8F5E9"
            advice = [
                "ยอดเยี่ยม! พฤติกรรมการทำงานของคุณอยู่ในเกณฑ์ดีมาก",
                "พยายามรักษาวินัยการออกกำลังกายอย่างสม่ำเสมอต่อไป",
                "อย่าลืมลุกยืดเส้นยืดสายเปลี่ยนอิริยาบถทุกๆ 1-2 ชั่วโมง"
            ]
        elif prediction == 'Medium':
            risk_text = "ความเสี่ยงปานกลาง (Medium Risk)"
            color = "#FF9800"
            bg_color = "#FFF3E0"
            advice = [
                "ควรเริ่มปรับเปลี่ยนพฤติกรรม เพื่อป้องกันอาการปวดเรื้อรัง",
                "ปรับระดับความสูงของจอคอมพิวเตอร์ให้อยู่ในระดับสายตาพอดี",
                "ตั้งนาฬิกาเตือนเพื่อลุกเดิน หรือยืดกล้ามเนื้อคอ บ่า ไหล่ ทุกๆ 1 ชั่วโมง"
            ]
        else:
            risk_text = "ความเสี่ยงสูง (High Risk) 🚨"
            color = "#F44336" 
            bg_color = "#FFEBEE"
            advice = [
                "อันตราย! คุณมีความเสี่ยงสูงมาก ควรปรับเปลี่ยนพฤติกรรมด่วน",
                "ตั้งเวลาเตือนพักยืดกล้ามเนื้อทุกๆ 45 นาทีอย่างเคร่งครัด",
                "พิจารณาเปลี่ยนไปใช้เก้าอี้และโต๊ะทำงานเพื่อสุขภาพ (Ergonomic)",
                "หากมีอาการปวดรุนแรงรบกวนการใช้ชีวิต ควรปรึกษาแพทย์หรือนักกายภาพบำบัด"
            ]
        
        return render_template('index.html', 
                               risk_level=risk_text, 
                               color=color, 
                               bg_color=bg_color,
                               advice_list=advice)
    except Exception as e:
        return render_template('index.html', error_text=f'เกิดข้อผิดพลาด: {str(e)}')

if __name__ == "__main__":
    app.run(debug=True)