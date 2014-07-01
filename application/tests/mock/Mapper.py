from models.abstract import DbMapper


class MockMapper(DbMapper.DbMapper):

    def add(self, writer):
        writer.onAdd()
        self.actionSave(writer)
        writer.onAfterAdd()

    def save(self, writer):
        writer.onUpdate()
        self.actionSave(writer)
