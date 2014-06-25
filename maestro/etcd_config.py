import etcd
import ast

def testfunction():
	with open('etcd_output.txt', 'w') as outfile:
		outfile.write("this is a test")


"""
 	write topology to etcd
	etcd should know where all cassandra nodes are
		under /cassandra there you have a dictionary of the cassandra nodes

"""
def register_with_etcd(container):
	client = etcd.Client()

	service_name = container._service.name
	instance_name = container.name
	instance_host = container._ship._ip
	instance_ports = container.ports

	instance_dict = {'service_name': service_name,
					 'instance_name': instance_name,
					 'instance_host': instance_host}

	etcd_key = "/"+service_name
	try:
		old_dict = client.read(etcd_key).value
	except:
		new_dict = {}
		client.write(etcd_key, new_dict)
	full_instances_dict = client.read(etcd_key).value
	full_instances_dict = ast.literal_eval(full_instances_dict)

	full_instances_dict[instance_name] = instance_dict
	client.write(etcd_key, full_instances_dict)
