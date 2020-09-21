import sys, pika, time


def main():
	credentials = pika.PlainCredentials('ofryadmin', 'ofryadmin')
	parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)

	with pika.BlockingConnection(parameters) as connection:
		channel = connection.channel()
		channel.exchange_declare(exchange='logs',
								 exchange_type='fanout')
		count = 0
		while True:
			message = f"Hello World! {count}"
			channel.basic_publish(exchange='logs',
			                      routing_key='',
			                      body=message)
			print(" [x] Sent %r" % message)
			count += 1
			time.sleep(1)


main()
