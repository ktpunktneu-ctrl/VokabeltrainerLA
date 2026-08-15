import sys, os, json, threading, webbrowser, socket, base64, io
from flask import Flask, request, jsonify, send_file

if getattr(sys, 'frozen', False):
    _BASE = os.path.dirname(sys.executable)
else:
    _BASE = os.path.dirname(os.path.abspath(__file__))

VOKABELN_PATH = os.path.join(_BASE, 'vokabeln.json')
_HTML = os.path.join(_BASE, 'index.html')
_TESSDATA_DIR = os.path.join(_BASE, 'tessdata')
_TESSERACT_EXE = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Flask(__name__, static_folder=os.path.join(_BASE, 'static'), static_url_path='/static')


def lade_vokabeln():
    if not os.path.exists(VOKABELN_PATH):
        return []
    with open(VOKABELN_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def speichere_vokabeln(vokabeln):
    with open(VOKABELN_PATH, 'w', encoding='utf-8') as f:
        json.dump(vokabeln, f, ensure_ascii=False, indent=2)


@app.route('/')
def index():
    resp = send_file(_HTML)
    resp.headers['Cache-Control'] = 'no-store'
    return resp


@app.route('/manifest.json')
def manifest():
    resp = send_file(os.path.join(_BASE, 'static', 'manifest.json'))
    resp.headers['Content-Type'] = 'application/manifest+json'
    return resp


@app.route('/sw.js')
def sw():
    resp = send_file(os.path.join(_BASE, 'static', 'sw.js'))
    resp.headers['Content-Type'] = 'application/javascript'
    return resp


@app.route('/api/vokabeln')
def api_vokabeln_list():
    resp = jsonify(lade_vokabeln())
    resp.headers['Cache-Control'] = 'no-store'
    return resp


@app.route('/api/kategorien')
def api_kategorien():
    vokabeln = lade_vokabeln()
    kategorien = sorted({v['kategorie'] for v in vokabeln})
    return jsonify(kategorien)


@app.route('/api/vokabeln', methods=['POST'])
def api_vokabeln_add():
    data = request.get_json()
    kategorie = (data.get('kategorie') or '').strip()
    it = (data.get('it') or '').strip()
    de = (data.get('de') or '').strip()
    if not kategorie or not it or not de:
        return jsonify(error='Kategorie, Latein und Deutsch sind Pflicht'), 400
    vokabeln = lade_vokabeln()
    neue_id = (max((v['id'] for v in vokabeln), default=0)) + 1
    eintrag = {'id': neue_id, 'kategorie': kategorie, 'it': it, 'de': de}
    vokabeln.append(eintrag)
    speichere_vokabeln(vokabeln)
    return jsonify(eintrag)


@app.route('/api/vokabeln/<int:vid>', methods=['PUT'])
def api_vokabeln_update(vid):
    data = request.get_json()
    vokabeln = lade_vokabeln()
    for v in vokabeln:
        if v['id'] == vid:
            v['kategorie'] = (data.get('kategorie') or v['kategorie']).strip()
            v['it'] = (data.get('it') or v['it']).strip()
            v['de'] = (data.get('de') or v['de']).strip()
            speichere_vokabeln(vokabeln)
            return jsonify(v)
    return jsonify(error='Nicht gefunden'), 404


@app.route('/api/vokabeln/<int:vid>', methods=['DELETE'])
def api_vokabeln_delete(vid):
    vokabeln = lade_vokabeln()
    neue = [v for v in vokabeln if v['id'] != vid]
    if len(neue) == len(vokabeln):
        return jsonify(error='Nicht gefunden'), 404
    speichere_vokabeln(neue)
    return jsonify(ok=True)


@app.route('/api/ocr', methods=['POST'])
def api_ocr():
    if not os.path.exists(_TESSERACT_EXE):
        return jsonify(error='Tesseract-OCR ist auf diesem Rechner nicht installiert.'), 500
    try:
        import pytesseract
        from PIL import Image
    except ImportError:
        return jsonify(error='pytesseract/Pillow fehlen (pip install pytesseract Pillow).'), 500

    data = request.get_json()
    b64 = (data.get('image') or '')
    if ',' in b64:
        b64 = b64.split(',', 1)[1]
    if not b64:
        return jsonify(error='Kein Bild übermittelt'), 400

    try:
        pytesseract.pytesseract.tesseract_cmd = _TESSERACT_EXE
        os.environ['TESSDATA_PREFIX'] = _TESSDATA_DIR
        img = Image.open(io.BytesIO(base64.b64decode(b64)))
        text = pytesseract.image_to_string(img, lang='lat+deu')
        return jsonify(text=text)
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.route('/api/shutdown', methods=['POST'])
def api_shutdown():
    def _stop():
        import time; time.sleep(0.4)
        os._exit(0)
    threading.Thread(target=_stop, daemon=True).start()
    return jsonify(ok=True)


def _lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return '127.0.0.1'


def _open_browser():
    import time; time.sleep(1.0)
    webbrowser.open('http://127.0.0.1:5058')


if __name__ == '__main__':
    ip = _lan_ip()
    print(f"Vokabeltrainer laeuft.")
    print(f"  Am PC:      http://127.0.0.1:5058")
    print(f"  Am iPhone:  http://{ip}:5058  (gleiches WLAN erforderlich)")
    threading.Thread(target=_open_browser, daemon=True).start()
    app.run(host='0.0.0.0', port=5058, debug=False, use_reloader=False)
