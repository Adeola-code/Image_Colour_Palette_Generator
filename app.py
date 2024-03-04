from flask import Flask, render_template, request
import numpy as np
from PIL import Image
from collections import Counter

app = Flask(__name__)



def get_top_colors(image_path, num_colors=10):
    # Load image and convert to NumPy array
    img = Image.open(image_path)
    img_array = np.array(img)

    # Flatten the image array and get color counts
    flat_img_array = img_array.reshape((-1, 3))
    color_counts = Counter(map(tuple, flat_img_array))

    # Get top N colors
    top_colors = color_counts.most_common(num_colors)

    return top_colors

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Check if the post request has the file part
        if 'file' not in request.files:
            return render_template('index.html', error="No file part")

        file = request.files['file']

        # Check if the file is empty
        if file.filename == '':
            return render_template('index.html', error="No selected file")

        # Check if the file is allowed
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            return render_template('index.html', error="Invalid file format")

        # Process the image and get top colors
        top_colors = get_top_colors(image_path=file)

        return render_template('result.html', top_colors=top_colors)

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
