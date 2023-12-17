from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey
import pandas as pd
import uuid
class Data(Base, BaseModel):
    __tablename__ = 'data'
    file_name = Column(String(128), nullable=False, index=True)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    
    user = relationship('User', back_populates='data')
    
    def __init__(self, file_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())
        self.file_name = file_name
    
    def read_data(self):
        df = pd.read_excel(f"data/dr/{self.file_name}")
        return df

    def save_df(self):
        df = self.read_data()
        name = self.file_name.split('.')[0]
        df.to_csv(f"data/df/{name}.csv", index=False)