from flask import Flask, request, jsonify
from flask_cors import CORS
from ai_assistant import AIAssistant
from code_executor import CodeExecutor
from file_manager import FileManager
from security_manager import SecurityManager

app = Flask(__name__)
CORS(app)

class AISandbox:
    def __init__(self):
        self.ai_assistant = AIAssistant()
        self.code_executor = CodeExecutor()
        self.file_manager = FileManager()
        self.security_manager = SecurityManager()

    def generate_code(self, prompt):
        return self.ai_assistant.generate_code(prompt)

    def execute_code(self, code):
        return self.code_executor.run(code)

    def manage_files(self, action, params):
        return self.file_manager.process(action, params)

sandbox = AISandbox()

@app.route('/generate_code', methods=['POST'])
def generate_code():
    prompt = request.json.get('prompt')
    code = sandbox.generate_code(prompt)
    return jsonify({"code": code})

@app.route('/execute_code', methods=['POST'])
def execute_code():
    code = request.json.get('code')
    result = sandbox.execute_code(code)
    return jsonify({"result": result})

@app.route('/file_operation', methods=['POST'])
def file_operation():
    action = request.json.get('action')
    params = request.json.get('params')
    result = sandbox.manage_files(action, params)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
