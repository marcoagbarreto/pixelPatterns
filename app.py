from flask import Flask, render_template, send_file
from PIL import Image
from io import BytesIO
import numpy as np
import random
import base64

app = Flask(__name__)

def square_matrix(size):
    return np.ones([size, size, 3], dtype = np.uint8)


def color_gen():
    return list(np.random.choice(range(256), size=3))


def color_tiles(M, size, colors):
    M[:,:,0] = colors[0][0]
    M[:,:,1] = colors[0][1]
    M[:,:,2] = colors[0][2]

    for col in range(size):
        for row in range(size):
            index = random.randint(0, len(colors)-1)
            M[col,row,0] = colors[index][0] # R
            M[col,row,1] = colors[index][1] # G
            M[col,row,2] = colors[index][2] # B

    return M

@app.route("/")
def hello():
    return render_template('index.html', title="Pixel Patterns")

@app.route("/getimage")
def get_img():
    n_colors = 3
    colors = [color_gen() for n in range(n_colors)]
    size = 64
    M = square_matrix(size)
    M = color_tiles(M, size, colors)

    buffer = BytesIO()
    img = Image.fromarray(M)
    img.save(buffer, format='PNG')
    buffer.seek(0)
    data = buffer.read()  # get data from file (BytesIO)
    data = base64.b64encode(data)  # convert to base64 as bytes
    data = data.decode()

    return data
    # response = send_file(buffer, mimetype='image/png')
    # return response


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)