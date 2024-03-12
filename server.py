import subprocess
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/download', methods=['GET'])
def download_video():
    # url = request.form.get('url')

    omakeurl = 'yt-dlp -f "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]" https://www.youtube.com/watch?v=xjfN8DFCBu0'

    # if not url:
    #     # URLが指定されていない場合
    #     return 'Error: URL is missing'

    try:
        # yt-dlpコマンドを実行
        result = subprocess.Popen(omakeurl, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        print("ダウンロードを開始します...", flush=True)

        while True:
            # プロセスの出力をリアルタイムで読み取る
            output = result.stdout.readline()   # 1行読み取る
            if output == '' and result.returncode is not None:  # プロセスが終了していたらループを抜ける
                break
            if output:
                yield output  # 1行返す

        # ダウンロードが正常に終了したかどうかを判定
        if result.returncode == 0:
            print("debug: Download successful", flush=True)
            return 'Download successful'
        else:
            print(f'Error: {result.stderr}', flush=True)
            return f'Error: {result.stderr}'
    except FileNotFoundError:
        # yt-dlpコマンドが見つからなかった場合
        print('Error: yt-dlp command not found', flush=True)
        return 'Error: yt-dlp command not found'

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=7000)