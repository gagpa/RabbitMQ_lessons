import sys, pika


def main():
	credentials = pika.PlainCredentials('ofryadmin', 'ofryadmin')
	parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)

	with pika.BlockingConnection(parameters) as connection:
		channel = connection.channel()
		channel.queue_declare(queue='task', durable=True)
		message = ' '.join(sys.argv[1:]) or "Hello World!"
		channel.basic_publish(exchange='',
		                      routing_key='task',
		                      body=message, 
		                      properties=pika.BasicProperties(delivery_mode=2))
		print(" [x] Sent %r" % message)


main()
