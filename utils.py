def is_auth(user_type, table):

    students_tables = ['classroom', 'course']
    teachers_tables = ['teaches', 'department']

    if user_type == 'student':
        if table not in students_tables:
            return False
        else:
            return True
    if user_type == 'teacher':
        if table not in teachers_tables:
            return False
        else:
            return True
