class SecurityManager:
    def __init__(self):
        # Базовые настройки безопасности
        self.allowed_operations = ['read', 'write', 'execute']
        self.max_file_size = 1024 * 1024  # 1 МБ
