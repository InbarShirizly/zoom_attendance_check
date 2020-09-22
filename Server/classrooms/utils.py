import secrets
import os

def save_file(form_file): #TODO: create better algorithem to save the files
    _, f_ext = os.path.splitext(form_file.filename) 
    file_name = secrets.token_hex(8) + f_ext
    file_path = os.path.join(app.root_path, 'static', 'students', file_name)
    form_file.save(file_path)
    return file_name
