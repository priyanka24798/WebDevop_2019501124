from models import Books


def getbooks(search_type,book_info):
    books = Books.query.order_by(Books.tittle.asc()).filter(getattr(Books, search_type).ilike(book_info)).all()
    return books

def getbook(isbn):
    book1 = Books.query.filter(Books.isbn == isbn).all()
    return book1