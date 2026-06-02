from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

SERVICE_KEY = 'e62d76c76fd300608912abda46bd7be3d631859463b4314fea20b66dcadb8715'
BASE_URL = 'https://apis.data.go.kr/1613000/RTMSDataSvcAptTradeDev/getRTMSDataSvcAptTradeDev'

@app.route('/api/apt', methods=['GET'])
def get_apt_data():
    lawd_cd = request.args.get('LAWD_CD', '')
    deal_ymd = request.args.get('DEAL_YMD', '')
    num_rows = request.args.get('numOfRows', '100')

    if not lawd_cd or not deal_ymd:
        return jsonify({'error': '지역코드와 연월을 입력해주세요'}), 400

    params = {
        'serviceKey': SERVICE_KEY,
        'LAWD_CD': lawd_cd,
        'DEAL_YMD': deal_ymd,
        'numOfRows': num_rows,
        'pageNo': '1'
    }

    try:
        res = requests.get(BASE_URL, params=params, timeout=10)
        return res.text, 200, {'Content-Type': 'application/xml'}
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print('=' * 40)
    print('✅ 부동산 API 서버 시작!')
    print('주소: http://localhost:5000')
    print('종료: Ctrl + C')
    print('=' * 40)
    app.run(host='0.0.0.0', port=5000, debug=False)