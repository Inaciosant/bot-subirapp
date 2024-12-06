from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/start-bot', methods=['POST'])
def start_bot():
    data = request.get_json()
    project_name = data['projectName']
    
    try:
        # Criar o diretório do projeto
        os.makedirs(f'./{project_name}')
        os.chdir(f'./{project_name}')
        
        # Rodar os comandos da Expo Dev
        subprocess.run(['npx', 'create-expo-app', project_name, '--template', 'blank'])
        subprocess.run(['npm', 'install'])
        subprocess.run(['npx', 'eas', 'init', '--id', 'expo-id'])

        # Aqui, adicione o comando para autenticar ou pegar o token da Expo Dev
        subprocess.run(['eas', 'login', '--token', 'expo-token'])

        return jsonify({"message": "Bot iniciado com sucesso!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
