import subprocess
import tempfile
import os

class CodeExecutor:
    def run(self, code):
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py') as temp_file:
            temp_file.write(code)
            temp_file_path = temp_file.name

        try:
            result = subprocess.run(
                ['python', temp_file_path], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            return {
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
        except subprocess.TimeoutExpired:
            return {'error': 'Код выполнялся слишком долго'}
        finally:
            os.unlink(temp_file_path)
