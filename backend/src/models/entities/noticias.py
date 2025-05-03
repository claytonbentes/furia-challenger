from src.models.settings.base import Base
from sqlalchemy import Column, String, DateTime

class Noticias(Base):
    __tablename__ = 'noticias'

    id = Column(String, primary_key=True)
    titulo = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    data = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"<Noticias(id={self.id}, titulo={self.titulo}, descricao={self.descricao}, data={self.data})>"
