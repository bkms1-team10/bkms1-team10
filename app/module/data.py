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



class User:
    def __init__(self, user_id=None, id=None, pw=None, nickname=None, email=None, address=None, address_gu=None, address_dong=None, lat_long=None, lat=None, long=None):
        self.__user_id = user_id
        self.__id = id
        self.__pw = pw
        self.__nickname = nickname
        self.__email = email
        self.__address = address
        self.__address_gu = address_gu
        self.__address_dong = address_dong
        self.__lat_long = lat_long
        self.__lat = lat
        self.__long = long 
    
    @property
    def user_id(self):
        return self.__user_id
    
    @user_id.setter
    def user_id(self, value):
        self.__user_id = value

    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, value):
        self.__id = value

    @property
    def pw(self):
        return self.__pw
    
    @pw.setter
    def pw(self, value):
        self.__pw = value
    
    @property
    def nickname(self):
        return self.__nickname
    
    @nickname.setter
    def nickname(self, value):
        self.__nickname = value
    
    @property
    def email(self):
        return self.__email
    
    @email.setter
    def email(self, value):
        self.__email = value

    @property
    def address(self):
        return self.__address
    
    @address.setter
    def address(self, value):
        self.__address = value
    
    @property
    def address_gu(self):
        return self.__address_gu
    
    @address_gu.setter
    def address_gu(self, value):
        self.__address_gu = value

    @property
    def address_dong(self):
        return self.__address_dong
    
    @address_dong.setter
    def address_dong(self, value):
        self.__address_dong = value
    
    @property
    def lat_long(self):
        return self.__lat_long
    
    @lat_long.setter
    def lat_long(self, value):
        self.__lat_long = value
    
    @property
    def lat(self):
        return self.__lat
    
    @lat.setter
    def lat(self, value):
        self.__lat = value

    @property
    def long(self):
        return self.__long
    
    @long.setter
    def long(self, value):
        self.__long = value
        