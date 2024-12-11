from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# 데이터베이스 초기화
def init_db():
    conn = sqlite3.connect('calculations.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS calculations (ip TEXT, expression TEXT, result TEXT)')
    conn.commit()
    conn.close()

def getip():
    return request.headers.get("CF-Connecting-IP", request.remote_addr)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# 계산 결과 저장
@app.route('/save', methods=['POST'])
def save_result():
    data = request.json
    expression = data.get('expression')
    result = data.get('result')
    conn = sqlite3.connect('calculations.db')
    c = conn.cursor()
    c.execute('INSERT INTO calculations (ip, expression, result) VALUES (?, ?, ?)', (getip(), expression, result))
    conn.commit()
    conn.close()
    return 'Saved', 200

# 저장된 기록 가져오기 (아이피 주소에 따라 필터링)
@app.route('/records', methods=['GET'])
def get_records():
    client_ip = getip()  # 클라이언트의 IP 주소 가져오기
    conn = sqlite3.connect('calculations.db')
    c = conn.cursor()
    c.execute('SELECT expression, result FROM calculations WHERE ip = ?', (client_ip,))
    records = c.fetchall()
    conn.close()
    return jsonify(records)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5004)  # 모든 IP에서 접근 가능