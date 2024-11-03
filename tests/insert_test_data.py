from app.db.database import SessionLocal
from app.db.models import Category, Subcategory

def insert_test_data():
    db = SessionLocal()
    try:
        # Insert categories
        electronics = Category(id=1, name='Electronics')
        books = Category(id=2, name='Books')
        db.add_all([electronics, books])
        db.commit()

        # Insert subcategories linked to the categories
        mobile_phones = Subcategory(id=1, name='Mobile Phones', category_id=1)
        laptops = Subcategory(id=2, name='Laptops', category_id=1)
        fiction = Subcategory(id=3, name='Fiction', category_id=2)
        non_fiction = Subcategory(id=4, name='Non-fiction', category_id=2)
        db.add_all([mobile_phones, laptops, fiction, non_fiction])
        db.commit()
    finally:
        db.close()

if __name__ == '__main__':
    insert_test_data()
