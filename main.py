from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, Field, create_engine
from typing import Optional
from sqlmodel import Session, select
from fastapi import HTTPException


# Database setup
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)

# --- Models ---

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float
    stock: int
    category: str

class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id")
    quantity: int
    customer_name: str
    status: str = "pending"

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"message": "Tote and Trend API is running"}
def get_session():
    with Session(engine) as session:
        yield session

# --- Create a product ---
@app.post("/products/")
def create_product(product: Product, session: Session = Depends(get_session)):
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

# --- Get all products ---
@app.get("/products/")
def read_products(session: Session = Depends(get_session)):
    products = session.exec(select(Product)).all()
    return products

# --- Get one product by ID ---
@app.get("/products/{product_id}")
def read_product(product_id: int, session: Session = Depends(get_session)):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# --- Update a product ---
@app.put("/products/{product_id}")
def update_product(product_id: int, updated: Product, session: Session = Depends(get_session)):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product.name = updated.name
    product.price = updated.price
    product.stock = updated.stock
    product.category = updated.category
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

# --- Delete a product ---
@app.delete("/products/{product_id}")
def delete_product(product_id: int, session: Session = Depends(get_session)):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    session.delete(product)
    session.commit()
    return {"message": "Product deleted"}
# --- Create an order (with stock check) ---
@app.post("/orders/")
def create_order(order: Order, session: Session = Depends(get_session)):
    product = session.get(Product, order.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if product.stock < order.quantity:
        raise HTTPException(
            status_code=400,
            detail=f"Not enough stock. Available: {product.stock}, requested: {order.quantity}"
        )
    
    product.stock -= order.quantity
    session.add(product)
    
    order.status = "confirmed"
    session.add(order)
    session.commit()
    session.refresh(order)
    return order

# --- Get all orders ---
@app.get("/orders/")
def read_orders(session: Session = Depends(get_session)):
    orders = session.exec(select(Order)).all()
    return orders

# --- Get one order by ID ---
@app.get("/orders/{order_id}")
def read_order(order_id: int, session: Session = Depends(get_session)):
    order = session.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

# --- Cancel an order (and restore stock) ---
@app.delete("/orders/{order_id}")
def cancel_order(order_id: int, session: Session = Depends(get_session)):
    order = session.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    product = session.get(Product, order.product_id)
    if product:
        product.stock += order.quantity
        session.add(product)
    
    order.status = "cancelled"
    session.add(order)
    session.commit()
    return {"message": "Order cancelled and stock restored"}
@app.delete("/products/{product_id}")
def delete_product(product_id: int, session: Session = Depends(get_session)):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    existing_orders = session.exec(
        select(Order).where(Order.product_id == product_id)
    ).all()
    if existing_orders:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete product with existing orders. Cancel or reassign orders first."
        )
    
    session.delete(product)
    session.commit()
    return {"message": "Product deleted"}