import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from functools import wraps
from auth.jwt_manager import gerar_token, verificar_token

app = Flask(__name__)

# Configurações da aplicação
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', '/default/path/to/upload')
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # Limite de 5 MB para uploads

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'erro': 'Token ausente'}), 401
        try:
            payload = verificar_token(token)
            return f(payload, *args, **kwargs)
        except Exception as e:
            return jsonify({'erro': str(e)}), 401
    return decorated_function

# Rota para upload de arquivos
@app.route('/upload', methods=['POST'])
@token_required
def upload_file(current_user):
    if 'file' not in request.files:
        return jsonify({'erro': 'Parte do arquivo ausente'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'erro': 'Nenhum arquivo selecionado'}), 400
    if file and file.filename.endswith('.csv'):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            file.save(file_path)
            return jsonify({'mensagem': 'Arquivo carregado com sucesso', 'caminho_do_arquivo': file_path}), 200
        except Exception as e:
            app.logger.error(f"Erro ao salvar o arquivo: {str(e)}")
            return jsonify({'erro': 'Erro interno do servidor'}), 500
    else:
        return jsonify({'erro': 'Formato de arquivo não suportado'}), 400

if __name__ == '__main__':
    app.run(debug=True)