from app.db.database import SessionLocal
from app.db.models import Category, Subcategory

def insert_test_data():
    db = SessionLocal()
    try:
        # Check if categories exist, add them only if they are absent
        if not db.query(Category).filter_by(name='Electronics').first():
            electronics = Category(id=1, name='Electronics')
            db.add(electronics)
        if not db.query(Category).filter_by(name='Books').first():
            books = Category(id=2, name='Books')
            db.add(books)
        db.commit()

        # Check if subcategories exist, add them only if they are absent
        if not db.query(Subcategory).filter_by(name='Mobile Phones').first():
            mobile_phones = Subcategory(id=1, name='Mobile Phones', category_id=1)
            db.add(mobile_phones)
        if not db.query(Subcategory).filter_by(name='Laptops').first():
            laptops = Subcategory(id=2, name='Laptops', category_id=1)
            db.add(laptops)
        if not db.query(Subcategory).filter_by(name='Fiction').first():
            fiction = Subcategory(id=3, name='Fiction', category_id=2)
            db.add(fiction)
        if not db.query(Subcategory).filter_by(name='Non-fiction').first():
            non_fiction = Subcategory(id=4, name='Non-fiction', category_id=2)
            db.add(non_fiction)
        db.commit()
    finally:
        db.close()

if __name__ == '__main__':
    insert_test_data()
