from src.models.settings.base import Base
from sqlalchemy import Column, String

class Players(Base):
    __tablename__ = 'players'

    id = Column(String, primary_key=True)
    nome = Column(String, nullable=False)
    nick = Column(String, nullable=False)
    sobrenome = Column(String, nullable=False)
    funcao = Column(String, nullable=False)

    def __repr__(self):
        return f"<Players(id={self.id}, nome={self.nome}, nick={self.nick}, sobrenome={self.sobrenome}, funcao={self.funcao})>"