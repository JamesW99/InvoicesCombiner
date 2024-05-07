from flask import Flask, request, send_file
import os
from PDFCombiner import PDFCombiner  # 正确导入PDFCombiner类
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
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>发票省纸合并</title>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background-color: #f4f4f9;
                margin: 0;
                padding: 20px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            form {
                background: white;
                padding: 40px;
                border-radius: 8px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            h1 {
                color: #333;
                text-align: center;
            }
            p {
                color: #666;
                text-align: center;
                margin-top: 0;
                margin-bottom: 20px; /* 添加底部边距 */

            }
            input[type="file"] {
                width: 100%;
                margin: 10px 0;
                padding: 10px;
                border: 2px dashed #ccc;
                display: block;
            }
            input[type="submit"] {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                cursor: pointer;
                width: 100%;
            }
            input[type="submit"]:hover {
                background-color: #45a049;
            }
        </style>
    </head>
    <body>
        <h1>这个网站能让您在一张A4纸中塞下三张发票</h1>
        <p></p>
        <p>点击说明下面灰色的 Choose File, 选择所有要打印的发票（拖动鼠标或者按住Ctrl）。<br>Select the PDF files you want to combine and upload them.</p>
        <p>点击 Open 按钮完成选择,再点击合并&下载<br>Click the big green button.</p>
        <p>合并文件将出现在您的下载文件夹中。<br>The combined file will be ready in download shortly after.</p>
        <form method="post" enctype="multipart/form-data">
          <input type="file" name="file" multiple>
          <input type="submit" value="合并&下载">
        </form>
        
        <h3>Powered by <a href="https://github.com/JamesW99/InvoicesCombine"> Yishan </a></h3>
    </body>
    </html>
    '''


if __name__ == '__main__':
    app.run(debug=True)

