from flask import Flask, request, send_file
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from PDFCombiner import PDFCombiner  # 正确导入PDFCombiner类
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    # 确保上传文件夹存在
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    if request.method == 'POST':
        uploaded_files = request.files.getlist('file')
        pdf_paths = []

        # 保存上传的PDF文件
        def secure_filename_with_chinese(filename):
            # 分割文件名和扩展名
            file_base, file_extension = os.path.splitext(filename)
            # 使用 uuid 生成唯一文件名，避免重名问题，同时保留原文件的扩展名
            return f"{uuid.uuid4()}{file_extension}"

        for file in uploaded_files:
            if file:
                filename = secure_filename_with_chinese(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                pdf_paths.append(file_path)

        # 实例化PDFCombiner并调用process_files方法
        combiner = PDFCombiner(pdf_paths)
        output_path = combiner.process_files()

        # 提供下载合并后的PDF
        return send_file(output_path, as_attachment=True)

    return '''
    <!doctype html>
    <title>Upload multiple PDF files</title>
    <h1>Upload multiple PDF files to combine them</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file multiple>
      <input type=submit value=Upload>
    </form>
    '''


if __name__ == '__main__':
    app.run(debug=True)

