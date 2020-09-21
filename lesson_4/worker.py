import pika, os, sys, time


def main():
	credentials = pika.PlainCredentials('ofryadmin', 'ofryadmin')
	parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)
	with pika.BlockingConnection(parameters) as connection:
		channel = connection.channel()
		channel.exchange_declare(exchange='direct_logs',
								 exchange_type='direct')
		result = channel.queue_declare(queue='', exclusive=True, durable=True)
		queue_name = result.method.queue

		severities = sys.argv[1:]

		if not severities:
		    sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
		    sys.exit(1)

		for severity in severities:
		    channel.queue_bind(exchange='direct_logs', queue=queue_name, routing_key=severity)

		def callback(ch, method, properties, body):
		    print(" [x] Received %r" % body.decode())
		    print(" [x] Done")
		    time.sleep(1)

		channel.queue_bind(exchange='logs', queue=queue_name)
		channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

		print('Waitig for messages. To exit press CTRL+C')
		channel.start_consuming()


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print('Interrupted')
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)

