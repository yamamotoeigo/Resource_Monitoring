import convert2json
from flask import Flask, jsonify, abort
import os


app = Flask(__name__)
# JSONファイルのパスを設定
# JSON_FILE_PATH = '/home/yamamoto/workspace/network_monitoring/192.168.2.2.json'

@app.route('/get_json', methods=['GET'])
def get_json_file():
    json_data = stat.save_to_json()
    try:
        if json_data:
            # return send_file(jason_data, mimetype='application/json')
            return json_data
        else:
            return abort(404, description="Resource not found")
    except Exception as e:
        return abort(500, description=f"Internal Server Error: {e}")

if __name__ == '__main__':
    stat = convert2json.CombinedInfo()
    app.run(host='0.0.0.0', port=5000)