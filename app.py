from flask import Flask, render_template, send_file, jsonify
import google_sheet_manager
import ics_generator

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/events')
def events():
    courses = google_sheet_manager.get_all_courses()
    events = []
    for index, row in courses.iterrows():
        events.append({
            'title': f"{row['object']} - {row['professor']}",
            'start': f"{row['start_date']}T{row['start_time']}",
            'end': f"{row['end_date']}T{row['end_time']}",
            'description': f"Room: {row['room']}",
            'location': row['location']
        })
    return jsonify(events)

@app.route('/planning.ics')
def serve_ics():
    ics_generator.create_ics_file()
    return send_file('planning.ics', mimetype='text/calendar')

if __name__ == '__main__':
    app.run(debug=True)
