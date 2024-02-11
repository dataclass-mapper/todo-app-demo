class NotFoundException(Exception):
    def __init__(self, entity: str, id: int):
        self.entity = entity
        self.id = id
