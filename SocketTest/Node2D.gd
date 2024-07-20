extends Node2D

# Server address and port
var server_address: String = "127.0.0.1"
var server_port: int = 12345
var tcp_client

func _ready():
	# Initialize the TCP client
	tcp_client = StreamPeerTCP.new()
	connect_to_server()

func connect_to_server():
	var error = tcp_client.connect_to_host(server_address, server_port)
	if error == OK:
		print("Connected to server.")
		# Start the connection monitoring process
		set_process(true)
	else:
		print("Failed to connect to server: ", error)

func _process(delta):
	# Check for incoming data
	tcp_client.poll()
	if tcp_client.get_available_bytes() > 0:
		var received_data = tcp_client.get_utf8_string(tcp_client.get_available_bytes())
		print("Received data: ", received_data)
	
	# Example of sending data periodically (for demo purposes)
	#send_message("Hello, Server!")

func send_message(message: String):
	tcp_client.put_utf8_string(message)
	tcp_client.put_u8(10)  # Adding a newline character for the server to recognize end of message
	var send_error = tcp_client.poll()
	if send_error != OK:
		print("Failed to send message: ", send_error)
	else:
		print("Message sent: ", message)

func _exit_tree():
	# Clean up the connection when exiting
	tcp_client.disconnect_from_host()
	print("Disconnected from server.")
