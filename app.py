import os
import io
from flask import Flask, request, jsonify, send_file
from PIL import Image
from rembg import remove

app = Flask(__name__)

@app.route('/')
def home():
    return "AI Background Changer API is Running Successfully!"

@app.route('/api/change-background', methods=['POST'])
def change_background():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    
    file = request.files['image']
    bg_color = request.form.get('background', 'white')
    
    try:
        input_image = Image.open(file.stream)
        output_image = remove(input_image)
        
        background = Image.new("RGBA", output_image.size, bg_color)
        final_image = Image.alpha_composite(background.convert("RGBA"), output_image.convert("RGBA"))
        
        img_io = io.BytesIO()
        final_image.convert("RGB").save(img_io, 'JPEG', quality=90)
        img_io.seek(0)
        
        return send_file(img_io, mimetype='image/jpeg')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
