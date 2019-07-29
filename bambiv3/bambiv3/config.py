import os #for enbironment variables

class Config:
	SECRET_KEY = '0a383bdacfada9ed7b9603837f78bb71'
	SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = 'bambichatter@gmail.com' #os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = '@bambichat' #os.environ.get('MAIL_PASSWORD')