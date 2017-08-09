from flask import request

from controller import application
from models import ServiceRegistry
from models import ServiceInstance

@application.route('/service-registry/')
@application.route('/service-registry/index')
def index():
	return "Service registry application"

@application.route('/service-registry/register', methods=['POST'])
def register():
	if request.json:
		service = request.json['service']
		host = request.json['host']
		port = request.json['port']
		health = request.json['health']
		service_data = ServiceRegistry.query.filter_by({'service': service})
		if service_data:
			service_instance_item = ServiceInstance(
				service_id=service_data.id,
				host=host,
				port=port,
				health=health
			)
			db.session.add(service_instance_item)
			db.session.commit()
		else:
			service_item = ServiceRegistry(
				service = service
			)
			db.session.add(service_item)
			db.session.commit()
			service_instance_item = ServiceInstance(
				service_id=service_item.id,
				host=host,
				port=port,
				health=health
			)
			db.session.add(service_instance_item)
			db.session.commit()
		return True
	return False

@application.route('/service-registry/deregister', methods=['POST'])
def deregister():
	if request.json:
		service = request.json['service']
		host = request.json['host']
		port = request.json['port']
		service_instance_data = ServiceInstance.filter_by(
			{
				'service_id':service,
				'host':host,
				'port':port
			}
		)
		db.session.delete(service_instance_data)
		return True
	return False

@application.route('/service-registry/heartbeat', methods=['POST'])
def heartbeat():
	if request.json:
		service = request.json['service']
		host = request.json['host']
		port = request.json['port']
		health = request.json['health']
		service_instance_data = ServiceInstance.query.filter_by(
			{
				'service_id':service,
				'host':host,
				'port':port,
				'health':health
			}
		)
		db.session.commit(service_instance_data)
		return True
	return False

@application.route('/service-registry/service-info/<service>', methods=['GET'])
def service_info(service):
	service_data = ServiceRegistry.filter_by(
		{
			'service':service
		}
	)
	service_instances_list = ServiceInstance.filter_by(
		{
			'service_id':service
		}
	)
	maximum_health = float('-inf')
	machine_details = None
	for service_instance in service_instances_list:
		if service_instances_list[service_instance].health > health:
			maximum_health = service_instances_list[service_instance].health
			machine_details = service_instance
	return machine_details

