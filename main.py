from bs4 import BeautifulSoup
from flask import Flask, request, redirect, url_for, render_template
import requests
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    meta_tags = soup.find_all('meta')
    for tag in meta_tags:
        if tag.get('property') == 'og:image':
            img_url = tag.get('content')
            response = requests.get(img_url)
            # Get the current user's home directory
            home_dir = os.path.expanduser("~")
            # Create a folder to save images
            os.makedirs(os.path.join(home_dir, 'instagram_images'), exist_ok=True)
            if not os.path.exists(os.path.join(home_dir, 'instagram_images')):
                os.makedirs(os.path.join(home_dir, 'instagram_images'))
            # Save the image in the 'instagram_images' folder with a unique name
            open(os.path.join(home_dir, 'instagram_images/image_{}.jpg'.format(len(os.listdir(os.path.join(home_dir, 'instagram_images'))))), 'wb').write(response.content)
            return redirect(url_for('success'))
    return redirect(url_for('error'))

@app.route('/success')
def success():
    return 'Image downloaded successfully'

@app.route('/error')
def error():
    return 'Error: Invalid URL or image not found'

if __name__ == '__main__':
    app.run()
