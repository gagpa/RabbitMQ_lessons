import pika, os, sys, time


def main():
	credentials = pika.PlainCredentials('ofryadmin', 'ofryadmin')
	parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)
	with pika.BlockingConnection(parameters) as connection:
		channel = connection.channel()

		channel.queue_declare(queue='task', durable=True)

		def callback(ch, method, properties, body):
		    print(" [x] Received %r" % body.decode())
		    time.sleep(body.count(b'.'))
		    print(" [x] Done")
		    ch.basic_ack(delivery_tag=method.delivery_tag)


		channel.basic_consume(queue='task', on_message_callback=callback)

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

