class ProcessResult:
    def __init__(self, file_name, sensitive_data, status):
        self.file_name = file_name
        self.sensitive_data = sensitive_data
        self.status = status

    def to_dict(self):
        return {
            "file_name": self.file_name,
            "sensitive_data": self.sensitive_data,
            "status": self.status
        }