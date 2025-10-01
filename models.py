from pydantic import BaseModel

class Product(BaseModel):
    id: int
    name: str
    price: float
    category: str
    description: str = ""
    in_stock: bool = True
    rating: float = 0.0
    
    def __str__(self):
        return f"{self.name} (${self.price}) - {self.category}"
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'category': self.category,
            'description': self.description,
            'in_stock': self.in_stock,
            'rating': self.rating
        }