from src.models.settings.base import Base
from sqlalchemy import Column, String, DateTime

class Partidas(Base):
    __tablename__ = 'partidas'

    id = Column(String, primary_key=True)
    adversario = Column(String, nullable=False)
    data = Column(DateTime, nullable=False)
    resultado = Column(String, nullable=False)
    campeonato = Column(String, nullable=False)

    def __repr__(self):
        return f"<Partidas(id={self.id}, adversario={self.adversario}, data={self.data}, resultado={self.resultado}, campeonato={self.campeonato})>"