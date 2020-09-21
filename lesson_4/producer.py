import sys, pika, time


def main():
	credentials = pika.PlainCredentials('ofryadmin', 'ofryadmin')
	parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)

	with pika.BlockingConnection(parameters) as connection:
		channel = connection.channel()
		channel.exchange_declare(exchange='direct_logs',
								 exchange_type='direct')
		count = 0
		severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
		while True:
			message = f"Hello World! {count} {severity}"
			channel.basic_publish(exchange='direct_logs',
			                      routing_key=severity,
			                      body=message)
			print(" [x] Sent %r" % message)
			count += 1
			time.sleep(1)


main()
