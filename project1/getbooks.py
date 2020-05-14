from models import Books


def getbooks(search_type,book_info):
    books = Books.query.order_by(Books.tittle.asc()).filter(getattr(Books, search_type).ilike(book_info)).all()
    return books