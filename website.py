from flask import Flask, request, Response, redirect
from uploader import upload
from os import listdir, mkdir
from sys import platform
import config
from werkzeug.utils import secure_filename


if 'links' not in listdir():
    mkdir('links')
    

def get_path(*path):
    if platform == 'win32':
        _path = '\\'.join(path)
    else:
        _path = '/'.join(path)
    return _path


class static:
    def __init__(self, x):
        self.x = x

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = config.max_file_size_mb * 1000 * 1000

@app.route('/')
def index():
    return f'''<body style="background-color: black;">
<title>Upload file</title>
<h1 style="color: white; text-align: center; font-family: Arial;">Upload file</h1>
<form action = "/upload" method = "POST" enctype="multipart/form-data">  
    <br style="line-height: 150%;">
    <input type="file" name="file" style="border-radius: 8px; color: white; display: block; margin: auto; border: none;" />
    <br style="line-height: 150%;">
    <input type="submit" value="Upload" style="border-radius: 8px; display: block; margin: auto; border: none; padding: 10px;">

</form>
</body>'''

@app.route('/upload', methods=['POST', 'GET'])
def upload_flask():
    if request.method == 'POST' and request.files['file'].filename != '':
        id = static(upload(request.files['file'].stream.read(), secure_filename(request.files['file'].filename))).x
        return redirect(f'/uploaded?id={id}')
    else:
        return redirect('/')

@app.route('/direct-download')
def direct_download():
    id = request.args.get('id', str)
    found = False
    for x in listdir('links'):
        if x == id:
            found = True
    if found:
        return Response(
            open(get_path('links', id, listdir(get_path('links', id))[0]), 'rb').read(),
            headers={'Content-disposition':
                    f'attachment; filename={listdir(get_path("links", id))[0]}'
                }
            )
    else:
        return 'id not found'


@app.route('/uploaded')
def uploaded():
    return f'''<body style="background-color: black;">
<h1 style="color: white; text-align: center; font-family: Arial;">Your file is now avalible on url:</h1>
<h2 style="color: white; font-family: Arial; text-align: center;">{request.url.split('/')[2]}/download?id={request.args.get('id')}</h2>
</body>'''

@app.route('/download')
def download_page():
    id = request.args.get('id', str)
    if id.split(' ') == []:
        return '''<body style="background-color: black">
<title>File not found.</title>
<h1 style="font-family: Arial; color: white; text-align: center;">Error</h1>
<hr style="color: white;">
<h3 style="font-family: Arial; color: white; text-align: center;">File not found.</h3>
</body>'''
    else:
        found = False
        for x in listdir('links'):
            if x == id:
                found = True
                break
        
        if found:
            return f'''<body style="background-color: black">
<title>Download {listdir(get_path('links', id))[0]}</title>
<h2 style="font-family: Arial; color: white; text-align: center;">Your file is ready to be downloaded.</h2>
<button class="button download" type="button" onclick="location.href='/direct-download?id={id}'" style="border-radius: 8px; background-color: white; color: black; display: block; margin-left: auto; margin-right: auto; border: none; padding: 20px;">Download</button>
</body>'''
        else:
            return '''<body style="background-color: black">
<h1 style="font-family: Arial; color: white; text-align: center;">Error</h1>
<hr style="color: white;">
<h3 style="font-family: Arial; color: white; text-align: center;">File not found.</h3>
</body>'''



@app.errorhandler(404)
def notfoundpage(error):
    return '''<body style="background-color: black">
<title>404</title>
<h1 style="font-family: Arial; color: white; text-align: center;">404</h1>
<hr style="color: white;">
<h3 style="font-family: Arial; color: white; text-align: center;">Page not found.</h3>
</body>'''

@app.errorhandler(413)
def largefilesize(error):
    return f'''<body style="background-color: black">
<title>413</title>
<h1 style="font-family: Arial; color: white; text-align: center;">413</h1>
<hr style="color: white;">
<h3 style="font-family: Arial; color: white; text-align: center;">File is bigger than {config.max_file_size_mb} MB.</h3>
</body>'''
app.run('0.0.0.0', '80', debug=True)
