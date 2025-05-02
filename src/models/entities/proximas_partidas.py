from src.models.settings.base import Base
from sqlalchemy import Column, String, DateTime

class ProximasPartidas(Base):
    __tablename__ = 'proximas_partidas'

    id = Column(String, primary_key=True)
    adversario = Column(String, nullable=False)
    data = Column(DateTime, nullable=False)
    campeonato = Column(String, nullable=False)

    def __repr__(self):
        return f"<ProximasPartidas(id={self.id}, adversario={self.adversario}, data={self.data}, campeonato={self.campeonato})>"
