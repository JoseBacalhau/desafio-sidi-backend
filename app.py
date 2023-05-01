from flask import Flask, jsonify, request
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['job_applications']


app = Flask(__name__)

@app.route('/gupy/check_job_id/<int:job_id>', methods=['GET'])
def check_job_id(job_id):
    job = db.jobs.find_one({'job_id': job_id})
    if job:
        return jsonify({'status': 'ok'})
    else:
        return jsonify({'status': 'error', 'message': 'Job not found'})

@app.route('/gupy/get_job_messages/<int:job_id>', methods=['GET'])
def get_job_messages(job_id):
    job = db.jobs.find_one({'job_id': job_id})
    if job:
        return jsonify({'eliminatory_messages': job['eliminatory_messages'], 'mandatory_messages': job['mandatory_messages']})
    else:
        return jsonify({'status': 'error', 'message': 'Job not found'})
    
@app.route('/gupy/job_application', methods=['POST'])
def job_application():
    data = request.json
    db.jobs.insert_one(data)
    return jsonify({'status': 'ok'})

@app.route('/sidi/job_application', methods=['POST'])
def job_application_sidi():
    data = request.json
    db.applications_sidi.insert_one(data)
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
