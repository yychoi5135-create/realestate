from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

SERVICE_KEY = 'e62d76c76fd300608912abda46bd7be3d631859463b4314fea20b66dcadb8715'

APIS = {
    'apt': 'https://apis.data.go.kr/1613000/RTMSDataSvcAptTradeDev/getRTMSDataSvcAptTradeDev',
    'officetel': 'https://apis.data.go.kr/1613000/RTMSDataSvcOffiTrade/getRTMSDataSvcOffiTrade',
    'land': 'https://apis.data.go.kr/1613000/RTMSDataSvcLandTrade/getRTMSDataSvcLandTrade',
    'sh': 'https://apis.data.go.kr/1613000/RTMSDataSvcSh/getRTMSDataSvcSh',
    'rh': 'https://apis.data.go.kr/1613000/RTMSDataSvcRhTrade/getRTMSDataSvcRhTrade',
    'building': 'https://apis.data.go.kr/1613000/RTMSDataSvcNrgCmplex/getRTMSDataSvcNrgCmplex',
}

@app.route('/')
def index():
    return send_file('apt-trade-radar.html')

@app.route('/apt-trade-radar.html')
def radar():
    return send_file('apt-trade-radar.html')

@app.route('/api/trade', methods=['GET'])
def get_trade_data():
    lawd_cd = request.args.get('LAWD_CD', '')
    deal_ymd = request.args.get('DEAL_YMD', '')
    num_rows = request.args.get('numOfRows', '100')
    trade_type = request.args.get('type', 'apt')

    if not lawd_cd or not deal_ymd:
        return jsonify({'error': '지역코드와 연월을 입력해주세요'}), 400

    base_url = APIS.get(trade_type, APIS['apt'])

    params = {
        'serviceKey': SERVICE_KEY,
        'LAWD_CD': lawd_cd,
        'DEAL_YMD': deal_ymd,
        'numOfRows': num_rows,
        'pageNo': '1'
    }

    try:
        res = requests.get(base_url, params=params, timeout=10)
        return res.text, 200, {'Content-Type': 'application/xml'}
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 기존 API 호환성 유지
@app.route('/api/apt', methods=['GET'])
def get_apt_data():
    return get_trade_data()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)