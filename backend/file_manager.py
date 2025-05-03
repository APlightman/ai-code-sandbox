import os
import shutil

class FileManager:
    BASE_DIR = '/sandbox/workspace'

    def __init__(self):
        os.makedirs(self.BASE_DIR, exist_ok=True)

    def process(self, action, params):
        methods = {
            'create_file': self.create_file,
            'read_file': self.read_file,
            'list_files': self.list_files
        }
        
        handler = methods.get(action)
        if handler:
            return handler(params)
        return {'error': 'Неизвестная операция'}

    def create_file(self, params):
        filepath = os.path.join(self.BASE_DIR, params['filename'])
        try:
            with open(filepath, 'w') as f:
                f.write(params.get('content', ''))
            return {'success': True, 'path': filepath}
        except Exception as e:
            return {'error': str(e)}

    def read_file(self, params):
        filepath = os.path.join(self.BASE_DIR, params['filename'])
        try:
            with open(filepath, 'r') as f:
                return {'content': f.read()}
        except Exception as e:
            return {'error': str(e)}

    def list_files(self, params):
        return {
            'files': os.listdir(self.BASE_DIR)
        }
