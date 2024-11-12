from app.db.database import SessionLocal
from app.db.models import Category, Subcategory

def insert_test_data():
    db = SessionLocal()
    try:
        # Check if categories exist, add them only if they are absent
        electronics = db.query(Category).filter_by(name='Electronics').first()
        if not electronics:
            electronics = Category(name='Electronics')
            db.add(electronics)

        books = db.query(Category).filter_by(name='Books').first()
        if not books:
            books = Category(name='Books')
            db.add(books)
        db.commit()

        # Check if subcategories exist, add them only if they are absent
        if not db.query(Subcategory).filter_by(name='Mobile Phones').first():
            mobile_phones = Subcategory(name='Mobile Phones', category_id=electronics.id)
            db.add(mobile_phones)
        if not db.query(Subcategory).filter_by(name='Laptops').first():
            laptops = Subcategory(name='Laptops', category_id=electronics.id)
            db.add(laptops)
        if not db.query(Subcategory).filter_by(name='Fiction').first():
            fiction = Subcategory(name='Fiction', category_id=books.id)
            db.add(fiction)
        if not db.query(Subcategory).filter_by(name='Non-fiction').first():
            non_fiction = Subcategory(name='Non-fiction', category_id=books.id)
            db.add(non_fiction)
        db.commit()
    finally:
        db.close()

if __name__ == '__main__':
    insert_test_data()
