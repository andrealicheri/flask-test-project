# WARNING! DO NOT TOUCH THIS FILE. EXTEND IT WITH backend.py INSTEAD!

from flask import Flask, Response, abort
import mimetypes
import os

## send_from_directory(), render_template(), etc. were not used because they don't work with Vercel
app = Flask(__name__)
@app.route('/')
def home():
    lib_string = ""
    file_list = os.listdir("src/lib/")
    for file_name in file_list:
        if os.path.isfile(os.path.join("src/lib/", file_name)):
            file_extension = os.path.splitext(file_name)[1]  # Get the file extension
            if file_extension == '.js':
                lib_string += '<script src="/lib/{}"></script>'.format(file_name)
            elif file_extension == ".css":
                lib_string += '<link rel="stylesheet" href="/lib/{}" />'.format(file_name)
    with open(os.path.join("src/routes/index.html" ), "r") as file:
        mime_type = "text/html"
        return Response(file.read().replace("</head>", lib_string + "</head>").encode('utf-8'), mimetype=mime_type)

@app.route('/assets/<path:file_path>')
def serve_app_files(file_path):
    full_path = os.path.join("public/" + file_path)
    try:
        with open(full_path, "rb") as file:
            mime_type, _ = mimetypes.guess_type(full_path)
            if mime_type is None:
                mime_type = 'application/octet-stream'
            return Response(file.read(), mimetype=mime_type)
    except FileNotFoundError:
        abort(404)

@app.route('/lib/<path:file_path>')
def serve_lib_files(file_path):
    full_path = os.path.join("src/lib/" + file_path)
    try:
        with open(full_path, "rb") as file:
            mime_type, _ = mimetypes.guess_type(full_path)
            if mime_type is None:
                mime_type = 'application/octet-stream'
            return Response(file.read(), mimetype=mime_type)
    except FileNotFoundError:
        abort(404)
    
@app.route("/<path:file_path>")
def use_template(file_path):
    
    full_path = os.path.join("src/routes/" + file_path + "/index.html" )
    file_list = os.listdir("src/lib/")
    lib_string = ""
    try:
        for file_name in file_list:
            if os.path.isfile(os.path.join("src/lib/", file_name)):
                file_extension = os.path.splitext(file_name)[1]  # Get the file extension
                if file_extension == '.js':
                    lib_string += '<script src="/lib/{}"></script>'.format(file_name)
                elif file_extension == ".css":
                    lib_string += '<link rel="stylesheet" href="/lib/{}" />'.format(file_name)
        with open(full_path, "r") as file:
            mime_type = "text/html"
            return Response(file.read().replace("</head>", lib_string + "</head>").encode('utf-8'), mimetype=mime_type)
    except FileNotFoundError:
        abort(404)

if __name__ == "__main__":
    app.run(debug=True)