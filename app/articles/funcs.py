from app.cca import CCA

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in CCA.ALLOWED_EXTENSIONS
