import subprocess
from flask import Flask, jsonify, request, make_response, send_file
from flask_cors import CORS
from werkzeug.serving import WSGIRequestHandler
from yt_dlp import YoutubeDL
import os

app = Flask(__name__)
CORS(app)

@app.route('/file_download', methods=["GET", "POST"])
def file_download():
    file_path = 'videofiles/' + request.get_json().get('videoTitle') + '.mp4'
    print(f'debug: ファイルパス={file_path}', flush=True)

    dir = os.getcwd()

    print("dir: " + dir)

    # responseを作成
    response = make_response()
    response.data = open(file_path, 'rb').read()
    response.headers['Content-Disposition'] = 'attachment; filename=omake.mp4'
    response.mimetype = 'video/mp4'

    return response


@app.route('/download', methods=["GET", "POST"])
def download_video():
    data = request.get_json()
    url = data.get('url')

    print(f'debug: URL={url}', flush=True)

    if not url:
        # URLが指定されていない場合
        return 'Error: URL is missing'

    omakeurl = 'yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]" --output "/videofiles/%(title)s.%(ext)s" --concurrent-fragments 5 ' + url


    try:
        # yt-dlpコマンドを実行
        print("ダウンロードを開始します...", flush=True)
        result = subprocess.run(omakeurl, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)


        # ダウンロードが正常に終了したかどうかを判定
        if result.returncode == 0:
            print("debug: Download successful", flush=True)
            response = {
                'message': 'Download successful'
            }
            return make_response(jsonify(response))
        else:
            print(f'Error: {result.stderr}', flush=True)
            response = {
                'message': f'Error: {result.stderr}'
            }
            return make_response(jsonify(response))
    except FileNotFoundError:
        # yt-dlpコマンドが見つからなかった場合
        print('Error: yt-dlp command not found', flush=True)
        response = {
            'message': 'Error: yt-dlp command not found'
        }
        return make_response(jsonify(response))

if __name__ == '__main__':
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app.debug = True
    app.run(host='127.0.0.1', port=7000)