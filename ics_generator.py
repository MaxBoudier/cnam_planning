from ics import Calendar, Event
from datetime import datetime
from zoneinfo import ZoneInfo
import google_sheet_manager

def create_ics_file():
    """
    Fetches all courses from the Google Sheet and generates an .ics file.
    """
    calendar = Calendar()
    courses = google_sheet_manager.get_all_courses()
    homework = google_sheet_manager.get_all_homework()

    for index, course in courses.iterrows():
        event = Event()
        event.name = f"{course['object']} - {course['professor']}"
        
        start_datetime_str = f"{course['start_date']} {course['start_time']}"
        end_datetime_str = f"{course['end_date']} {course['end_time']}"
        
        start_datetime = datetime.strptime(start_datetime_str, "%d/%m/%Y %H:%M:%S").replace(tzinfo=ZoneInfo("Europe/Paris"))
        end_datetime = datetime.strptime(end_datetime_str, "%d/%m/%Y %H:%M:%S").replace(tzinfo=ZoneInfo("Europe/Paris"))

        event.begin = start_datetime
        event.end = end_datetime
        event.location = course['location']

        # Add homework to description
        course_homework = homework[homework['course_name'] == course['object']]
        description = f"Room: {course['room']}\n"
        if not course_homework.empty:
            description += "Homework:\n"
            for hw_index, hw in course_homework.iterrows():
                description += f"- {hw['description']} (Due: {hw['due_date']})\n"

        event.description = description
        
        calendar.events.add(event)

    with open("planning.ics", "w") as f:
        f.writelines(calendar)

if __name__ == '__main__':
    create_ics_file()
