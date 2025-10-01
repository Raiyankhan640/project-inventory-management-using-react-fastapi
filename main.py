from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import Product
import database_models
from database import SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database_models.Base.metadata.create_all(bind=SessionLocal().get_bind())

products = [
    Product(
        id=1,
        name="Wireless Bluetooth Headphones",
        price=79.99,
        category="Electronics",
        description="Noise-cancelling wireless headphones with 30hr battery life",
        in_stock=True,
        rating=4.5
    ),
    Product(
        id=2,
        name="Stainless Steel Water Bottle",
        price=24.99,
        category="Home & Kitchen",
        description="Insulated 32oz water bottle, keeps drinks cold for 24hrs",
        in_stock=True,
        rating=4.8
    ),
    Product(
        id=3,
        name="Organic Cotton T-Shirt",
        price=19.99,
        category="Clothing",
        description="100% organic cotton, available in multiple colors",
        in_stock=False,
        rating=4.3
    ),
    Product(
        id=4,
        name="Smart Fitness Tracker",
        price=129.99,
        category="Electronics",
        description="Track heart rate, sleep, and daily activity",
        in_stock=True,
        rating=4.6
    ),
    Product(
        id=5,
        name="Ceramic Coffee Mug Set",
        price=34.99,
        category="Home & Kitchen",
        description="Set of 4 handmade ceramic mugs",
        in_stock=True,
        rating=4.7
    ),
    Product(
        id=6,
        name="Gaming Mechanical Keyboard",
        price=89.99,
        category="Electronics",
        description="RGB backlit mechanical keyboard with customizable keys",
        in_stock=True,
        rating=4.4
    ),
    Product(
        id=7,
        name="Yoga Mat Premium",
        price=45.99,
        category="Sports & Fitness",
        description="Non-slip eco-friendly yoga mat with carrying strap",
        in_stock=True,
        rating=4.9
    ),
    Product(
        id=8,
        name="Wireless Phone Charger",
        price=29.99,
        category="Electronics",
        description="Fast charging pad compatible with all Qi-enabled devices",
        in_stock=False,
        rating=4.2
    ),
    Product(
        id=9,
        name="Leather Wallet",
        price=59.99,
        category="Accessories",
        description="Genuine leather bifold wallet with RFID protection",
        in_stock=True,
        rating=4.5
    ),
    Product(
        id=10,
        name="Bamboo Cutting Board",
        price=39.99,
        category="Home & Kitchen",
        description="Eco-friendly bamboo cutting board set of 3 sizes",
        in_stock=True,
        rating=4.6
    )
]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.on_event("startup")
def init_db():
    db = SessionLocal()
    # Delete all existing products
    db.query(database_models.Product).delete()
    db.commit()
    # Insert sample products
    for product in products:
        db_product = database_models.Product(
            id=product.id,
            name=product.name,
            price=product.price,
            category=product.category,
            description=product.description,
            in_stock=product.in_stock,
            rating=product.rating
        )
        db.add(db_product)
    db.commit()
    print("Products inserted into DB:", db.query(database_models.Product).all())
    db.close()

@app.get("/products")
async def get_products(db: Session = Depends(get_db)):
    products = db.query(database_models.Product).all()
    return products

@app.get("/products/{product_id}")
async def get_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == product_id).first()
    if db_product is None:
        return {"error": "Product not found"}
    return db_product

@app.post("/products")
async def create_product(product: Product, db: Session = Depends(get_db)):
    db_product = database_models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.put("/products/{product_id}")
def update_product(product_id: int, product: Product, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == product_id).first()
    if db_product:
        db_product.name = product.name
        db_product.price = product.price
        db_product.category = product.category
        db_product.description = product.description
        db_product.in_stock = product.in_stock
        db_product.rating = product.rating
        db.commit()
        db.refresh(db_product)
        return db_product
    else:
        return {"error": "Product not found"}

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(database_models.Product).filter(database_models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"detail": "Product deleted"}