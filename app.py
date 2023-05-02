from flask import Flask, jsonify, request
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
dbgupy = client['GUPY']
dbsidi = client['SIDI']

app = Flask(__name__)

@app.route('/gupy/check_job_id/<int:job_id>', methods=['GET'])
def check_job_id(job_id):
    job = dbgupy.check_job_id.find_one({'job_id': job_id})
    if job:
        return jsonify([{'Status': 'OK'},{'job': job.get('job')}])
    else:
        return jsonify({'status': 'error', 'message': 'Job not found'})

@app.route('/gupy/get_job_messages', methods=['GET'])
def get_job_messages():
    job = dbgupy.get_job_messages.find_one()
    if job:
        return jsonify({'Pergunta ELiminatória': job.get('Pergunta ELiminatória'), 'Pergunta Obrigatória': job.get('Pergunta Obrigatória')})
    else:
        return jsonify({'message': 'Nenhum job encontrado'})

@app.route('/gupy/job_application', methods=['POST'])
def job_application():
    experiencia = request.args.get('Você tem experiência na área desejada')
    conhecimentoIngles = request.args.get('Você tem conhecimento do idioma inglês intermediário / avançado?')
    conhecimentoPython = request.args.get('Você tem conhecimento em python?')
    nome = request.args.get('Qual seu nome?')
    email = request.args.get('Qual seu email?')
    formacao = request.args.get('Qual sua formação?')
    data = {
        'Você tem experiência na área desejada': experiencia,
        'Você tem conhecimento do idioma inglês intermediário / avançado?': conhecimentoIngles,
        'Você tem conhecimento em python?': conhecimentoPython,
        'Qual seu nome?': nome,
        'Qual seu email?': email,
        'Qual sua formação?': formacao
    }
    dbgupy.job_application.insert_one(data)

    return jsonify({'status': 'ok'})

@app.route('/sidi/job_application', methods=['POST'])
def job_application_sidi():
    data = request.json
    dbsidi.job_application.insert_one(data)
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
