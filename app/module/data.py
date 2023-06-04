class Book:
    def __init__(self, book_id=None, title=None, author=None, image_url=None, description=None, average_rating=None):
        self.__book_id = book_id
        self.__title = title
        self.__author = author
        self.__image_url = image_url
        self.__description = description
        self.__average_rating = average_rating
    
    @property
    def book_id(self):
        return self.__book_id
    
    @book_id.setter
    def book_id(self, value):
        self.__book_id = value

    @property
    def title(self):
        return self.__title
    
    @title.setter
    def title(self, value):
        self.__title = value

    @property
    def author(self):
        return self.__author
    
    @author.setter
    def author(self, value):
        self.__author = value
    
    @property
    def image_url(self):
        return self.__image_url
    
    @image_url.setter
    def image_url(self, value):
        self.__image_url = value
    
    @property
    def description(self):
        return self.__description
    
    @description.setter
    def description(self, value):
        self.__description = value

    @property
    def average_rating(self):
        return self.__average_rating
    
    @average_rating.setter
    def average_rating(self, value):
        self.__average_rating = value