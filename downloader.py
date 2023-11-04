from flask import Flask, send_file, jsonify
from pytube import YouTube
from flask_cors import CORS
from flask import request
import os

app = Flask(__name__)
CORS(app)


base_dir = os.path.abspath(os.path.dirname(__file__))
video_directory = os.path.join(base_dir, 'videos')

video_path = None

@app.route('/video')
def video():
    global video_path
    if video_path:
        return send_file(video_path, as_attachment=True)
    else:
        return "Error: Video not found"

@app.route('/descargar_video')
def descargar_video():
    global video_path
    print(request.args.get('link'))
    link = request.args.get('link')
    video_path = Download(link)

    if video_path:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})

def Download(link):
    youtubeObject = YouTube(link)
    video_title = youtubeObject.title
    video_path = os.path.join(video_directory, f'{video_title}.mp4')

    # Comprueba si el archivo ya existe en la carpeta
    if os.path.exists(video_path):
        print(f"El video '{video_title}' ya existe.")
        return video_path
    else:
        video_stream = youtubeObject.streams.get_highest_resolution()
        try:
            video_stream.download(output_path=video_directory, filename=f"{video_title}.mp4")
            print("Download is completed successfully")
            return video_path
        except:
            print("An error has occurred")
            return None

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
