import requests

"""
Input must be formatted as 127
"""
def lookup_class(code):
    courses = requests.get('https://www.berkeleytime.com/api/enrollment/enrollment_json/').json().get('courses')
    code = code.lower()

    if code.startswith('eecs'):
        code = code.replace('eecs', '').strip()
    elif code.startswith('cs'):
        code = code.replace('cs', '').strip()
    elif code.startswith('ee'):
        code = code.replace('ee', '').strip()
    else:
        code = code.strip()
    prefixes = ['COMPSCI', 'EECS', 'ELENG']

    print(code, prefixes)
    course_id, course_name = None, None
    for c in courses:
        if c.get('course_number') == code and c.get('abbreviation') in ['COMPSCI', 'EECS', 'EL ENG']:
            course_id = c.get('id')
            dept = c.get('abbreviation')
            number = c.get('course_number')
            course_name = dept + ' ' + number
            break
    
    if course_id != None and course_name != None:
        data = requests.get(f'https://www.berkeleytime.com/api/enrollment/aggregate/{course_id}/fall/2020/').json()
        data.get('title')
        wl = data.get('data')[-1].get('waitlisted')
        el = data.get('data')[-1].get('enrolled')
        em = data.get('data')[-1].get('enrolled_max')
        return f'Course Enrollment for {course_name}:\nEnrolled: {el}/{em}\nWaitlisted: {wl}'
    
    else:
        raise Exception("Something bad happened.")