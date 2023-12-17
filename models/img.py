from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey
import uuid
class Img(Base, BaseModel):
    __tablename__ = 'img'
    img_name = Column(String(128), nullable=False, index=True)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    
    user = relationship('User', back_populates='img')
    
    def __init__(self, img_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())
        self.img_name = img_name
