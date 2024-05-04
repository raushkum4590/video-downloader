from flask import Flask, request, render_template, send_file
from pytube import YouTube
import os

app = Flask(__name__)

@app.route('/')
def index():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouTube Video Downloader</title>
    <style>
        body {
            font-family: Arial, sans-serif;
        }

        .container {
            max-width: 500px;
            margin: 50px auto;
            padding: 20px;
            border: 1px solid #ccc;
            border-radius: 5px;
            background-color: #f9f9f9;
        }

        h1 {
            text-align: center;
        }

        label {
            font-weight: bold;
        }

        input[type="text"],
        select {
            width: 100%;
            padding: 10px;
            margin: 5px 0;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
        }

        input[type="submit"] {
            width: 100%;
            background-color: #4CAF50;
            color: white;
            padding: 14px 20px;
            margin: 8px 0;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }

        input[type="submit"]:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>YouTube Video Downloader</h1>
        <form action="/download" method="post">
            <label for="youtube_url">Enter YouTube URL:</label><br>
            <input type="text" id="youtube_url" name="youtube_url" required><br><br>
            <label for="format">Select Format:</label>
            <select id="format" name="format">
                <option value="mp4">MP4</option>
                <option value="mp3">MP3</option>
            </select><br><br>
            <label for="quality">Select Quality:</label>
            <select id="quality" name="quality">
                <option value="highest">Highest</option>
                <option value="lowest">Lowest</option>
            </select><br><br>
            <input type="submit" value="Download">
        </form>
    </div>
</body>
</html>
"""

@app.route('/download', methods=['POST'])
def download():
    if request.method == 'POST':
        youtube_url = request.form['youtube_url']
        format = request.form['format']
        quality = request.form['quality']
        try:
            yt = YouTube(youtube_url)
            if format == 'mp4':
                if quality == 'highest':
                    video = yt.streams.filter(progressive=True, file_extension='mp4').first()
                else:
                    video = yt.streams.filter(progressive=True, file_extension='mp4').last()
                download_dir = './videos'
                os.makedirs(download_dir, exist_ok=True)
                filename = video.default_filename
            elif format == 'mp3':
                audio = yt.streams.filter(only_audio=True).first()
                download_dir = './audios'
                os.makedirs(download_dir, exist_ok=True)
                filename = audio.default_filename
            file_path = os.path.join(download_dir, filename)
            if format == 'mp4':
                video.download(download_dir)
            elif format == 'mp3':
                audio.download(download_dir)
            return send_file(file_path, as_attachment=True)
        except Exception as e:
            return str(e)

if __name__ == '__main__':
    app.run(debug=True)
