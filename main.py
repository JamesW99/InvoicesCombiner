from flask import Flask, request, send_from_directory, render_template_string
import os
# from PyPDF2 import PdfMerger

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def combine(pdf_files):
    # merger = PdfMerger()
    # for pdf in pdf_files:
    #     merger.append(pdf)
    # combined_path = os.path.join(UPLOAD_FOLDER, 'combined.pdf')
    # merger.write(combined_path)
    # merger.close()
    # return combined_path
    pass
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        files = request.files.getlist('file')
        saved_files = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = file.filename
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                saved_files.append(filepath)
        if saved_files:
            combined_path = combine(saved_files)
            return render_template_string('''
                File(s) uploaded and combined successfully. <br>
                <a href="/download/combined.pdf">Download Combined PDF</a>.
            ''')
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new PDF file(s)</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file multiple>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
