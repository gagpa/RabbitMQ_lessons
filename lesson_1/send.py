import pika

def main():
	credentials = pika.PlainCredentials('ofryadmin', 'ofryadmin')
	parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)

	with pika.BlockingConnection(parameters) as connection:
		channel = connection.channel()
		channel.queue_declare(queue='hello')
		channel.basic_publish(exchange='',
							  routing_key='hello',
							  body='Hello World')


		print('Sent "Hello World!"')


main()
