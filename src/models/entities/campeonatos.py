from src.models.settings.base import Base
from sqlalchemy import Column, String, DateTime

class Campeonatos(Base):
    __tablename__ = 'campeonatos'

    id = Column(String, primary_key=True)
    nome = Column(String, nullable=False)
    data_inicio = Column(DateTime, nullable=False)
    data_fim = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)

    def __repr__(self):
        return f"<Campeonatos(id={self.id}, nome={self.nome}, data_inicio={self.data_inicio}, data_fim={self.data_fim}, status={self.status})>"
