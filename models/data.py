from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, LargeBinary, ForeignKey
import uuid
class Data(Base, BaseModel):
    __tablename__ = 'data'
    file_name = Column(String(128), nullable=False, index=True)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    
    user = relationship('User', back_populates='data')
    
    def __init__(self, file_name, user_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())
        self.file_name = file_name
        self.user_id = user_id