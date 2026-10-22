import os
import io
from flask import Flask, request, jsonify, send_file
from PIL import Image
from rembg import remove

app = Flask(__name__)

@app.route('/')
def home():
    return "AI Background Changer API with Themes is Live!"

@app.route('/api/change-background', methods=['POST'])
def change_background():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    
    file = request.files['image']
    bg_option = request.form.get('background', 'white').lower()
    
    try:
        input_image = Image.open(file.stream).convert("RGBA")
        
        # 1. AI ki madad se background remove karna
        output_image = remove(input_image)
        size = output_image.size
        
        # 2. Background option ke hisab se set karna
        if bg_option == 'garden' or bg_option == 'summer':
            # Garden / Summer ke liye natural green/outdoor tone ya scenic background
            background = Image.new("RGBA", size, (120, 200, 120, 255)) # Nature green tone
        elif bg_option == 'sky' or bg_option == 'blue':
            background = Image.new("RGBA", size, (135, 206, 235, 255)) # Sky blue tone
        else:
            # Agar koi solid color ya hex code bheja ho (jaise white, red, etc.)
            background = Image.new("RGBA", size, bg_option)
            
        # Foreground person ko background ke upar merge karna
        final_image = Image.alpha_composite(background, output_image)
        
        # Output image ko JPEG format me return karna
        img_io = io.BytesIO()
        final_image.convert("RGB").save(img_io, 'JPEG', quality=90)
        img_io.seek(0)
        
        return send_file(img_io, mimetype='image/jpeg')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
