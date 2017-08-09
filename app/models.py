from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from controller import application, db
from logger import create_logger

logger = create_logger('service-registry.log')

class ServiceRegistry(db.Model):

	__tablename__ = "service_registry"
	id = db.Column(db.Integer, primary_key=True)
	service = db.Column(db.String(255), unique=True, nullable=False)
	created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(
    	db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

class ServiceInstance(db.Model):

	__tablename__ = "service_instance"
	service_id = db.Column(db.Integer, db.ForeignKey('service_registry.id'), 
		primary_key=True)
	host = db.Column(db.String(255), nullable=False, primary_key=True)
	port = db.Column(db.String(255), nullable=False, primary_key=True)
	health = db.Column(db.Integer)
	created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(
    	db.DateTime, server_default=db.func.now(), onupdate=db.func.now())