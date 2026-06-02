from flask import Flask, render_template, request

app = Flask(__name__)

# Scoring Maps (Normalized to 4.0 scale)
GRADING_SYSTEMS = {
    "Standard": {"A+": 4.0, "A": 4.0, "A-": 3.7, "B+": 3.3, "B": 3.0, "B-": 2.7, "C+": 2.3, "C": 2.0, "D": 1.0, "F": 0.0},
    "IB": {"7": 4.0, "6": 3.7, "5": 3.3, "4": 2.7, "3": 2.0, "2": 1.0, "1": 0.0},
    "AP": {"5": 4.0, "4": 3.7, "3": 3.0, "2": 2.0, "1": 0.0},
    "IGCSE": {"9": 4.0, "8": 4.0, "7": 3.7, "6": 3.3, "5": 3.0, "4": 2.7, "3": 2.0, "2": 1.0, "1": 0.0},
    "A-Level": {"A*": 4.0, "A": 4.0, "B": 3.3, "C": 2.7, "D": 2.0, "E": 1.0}
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        class_name = request.form.get('class')
        system = request.form.get('system')
        subjects = request.form.getlist('subject')
        grades = request.form.getlist('grade')
        
        report_data = []
        total_gp = 0
        
        for i in range(len(subjects)):
            # Normalize grade to string for dictionary lookup
            grade_val = str(grades[i]).upper()
            gp = GRADING_SYSTEMS[system].get(grade_val, 0.0)
            report_data.append({"subject": subjects[i], "grade": grades[i], "gp": gp})
            total_gp += gp
            
        gpa = total_gp / len(subjects) if subjects else 0
        return render_template('report.html', name=name, class_name=class_name, 
                               system=system, report=report_data, gpa=round(gpa, 2))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)