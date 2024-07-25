from flask import Flask, request, send_file, send_from_directory
import qrcode
import io

app = Flask(__name__)

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/generate', methods=['POST'])
def generate():
    url = request.form.get('url')
    if not url:
        return "URL is required", 400

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')

    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)

    return send_file(buf, mimetype='image/png', as_attachment=True, download_name='qrcode.png')

if __name__ == '__main__':
    app.run(debug=True)
