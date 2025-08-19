from flask import Flask, request, render_template
import os
import configparser

CONFIG_FILE = 'config.ini'

# Buat config.ini jika belum ada
if not os.path.exists(CONFIG_FILE):
    config = configparser.ConfigParser()
    config['server'] = {'port': '5000'}
    config['settings'] = {'upload_folder': 'uploads'}
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)
    print(f"{CONFIG_FILE} dibuat dengan nilai default.")
else:
    print(f"{CONFIG_FILE} ditemukan, menggunakan konfigurasi yang ada.")

# Load konfigurasi
config = configparser.ConfigParser()
config.read(CONFIG_FILE)

PORT = int(config['server'].get('port', 5000))
UPLOAD_FOLDER = config['settings'].get('upload_folder', 'uploads')

# Setup Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file and file.filename:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return 'OK'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=False)