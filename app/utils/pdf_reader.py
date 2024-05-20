import PyPDF2


def read_pdf(cv_filepath):
    with open(cv_filepath, 'rb') as file:
        cv = PyPDF2.PdfReader(file)
        cv_input = ""
        for page in cv.pages:
            cv_input += page.extract_text()
    return cv_input
