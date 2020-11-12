import uuid


class IDGenerator:
    @staticmethod
    def generate_uuid():
        return str(uuid.uuid4()).replace("-", "")
