from flask import Flask, request, render_template, send_file
from pytube import YouTube
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

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
