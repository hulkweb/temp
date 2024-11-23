from flask import Flask, request, send_file, jsonify
from rembg import remove
from PIL import Image
import io
import os

app = Flask(__name__)

# Create an upload folder for temporary storage
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/remove-bg', methods=['POST'])
def remove_background():
    # Check if an image file is provided
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files['image']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Ensure the file is an image
    try:
        input_image = file.read()  # Read the uploaded file as binary
    except Exception as e:
        return jsonify({"error": "Invalid image file", "details": str(e)}), 400

    # Remove the background
    try:
        output_image = remove(input_image)  # Get processed image data
        
        # Write the output to a BytesIO object
        buffer = io.BytesIO(output_image)
        buffer.seek(0)  # Reset buffer pointer

        # Return the output image as a response
        return send_file(
            buffer,
            mimetype='image/png',
            as_attachment=True,
            download_name='output_image.png'
        )
    except Exception as e:
        return jsonify({"error": "Failed to process image", "details": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

