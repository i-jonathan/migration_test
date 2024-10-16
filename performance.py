import argparse
import subprocess
import time

import psutil


def extended_performance(command: str):
	"""
	Executes a shell command and measures its performance in terms of CPU usage, memory consumption, and execution time.

	Args:
		command (str): The shell command to be executed.

	Functionality:
	- Starts a subprocess to execute the given shell command.
	- Monitors CPU and memory usage of the process at 1-second intervals using the psutil library.
	- Calculates the average CPU and memory usage during the execution of the command.
	- Measures the total elapsed time from the start to the end of the process.

	Output:
	- Prints the output of the command, any errors, the total execution time, and average resource usage (CPU and memory).

	Exceptions:
		Handles psutil.NoSuchProcess exception if the process terminates prematurely.

	Returns:
		None. The function prints the results directly.

	Example usage:
		extended_performance('ls -la')

	:param command: The shell command to be executed.
	:return: None. The function prints the results directly.
	"""
	start = time.time()
	process = subprocess.Popen(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

	p_util = psutil.Process(process.pid)
	memory = []
	cpu = []

	try:
		while process.poll() is None:
			cpu_usage = p_util.cpu_percent(interval=1)
			memory_usage = p_util.memory_info().rss / (1024 * 1024)
			memory.append(memory_usage)
			cpu.append(cpu_usage)
			time.sleep(1)  # every second

	except psutil.NoSuchProcess:
		print('Process terminated before completion')

	end_time = time.time()
	elapsed_time = end_time - start
	average_memory = sum(memory) / len(memory) if memory else 0
	average_cpu = sum(cpu) / len(cpu) if cpu else 0

	print(f'Output: {process.stdout.read()}')
	print(f'Errors: {process.stderr}\n')
	print(f'Time: {elapsed_time:.4f} seconds')
	print(f'Average memory usage: {average_memory:.2f}MB')
	print(f'Average CPU usage: {average_cpu:.2f}%')


def basic_performance(command):
	"""
	Executes a shell command and measures its execution time.

	Args:
		command (str): The shell command to be executed.

	Functionality:
	- Runs the provided shell command using `subprocess.run`.
	- Captures the command's output and any errors using `stdout` and `stderr`.
	- Measures the total time taken to execute the command.

	Output:
	- Prints the command's output, any errors encountered during execution, and the time taken for the command to complete.

	Returns:
		None. The function prints the results directly.

	Example usage:
		basic_performance('ls -la')
	"""
	start = time.time()
	process = subprocess.run(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	end_time = time.time()
	elapsed_time = end_time - start

	print(f'Output: {process.stdout}')
	print(f'Errors: {process.stderr}\n')
	print(f'Time: {elapsed_time:.4f} seconds')


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Basic or Extended Performance Test.")
	parser.add_argument(
		'-t', '--type', required=True,
		help=
		'Type of performance test to execute (basic or extended).\n'
		'Options: '
		'basic: Only checks the time.'
		'extended: Checks the time, average memory and average CPU usage.'
	)
	parser.add_argument(
		'-c', '--command', required=True, nargs=argparse.REMAINDER,
		help='The command to be evaluated.'
	)

	args = parser.parse_args()

	command_to_run = ' '.join(args.command)
	print(f'Command: {command_to_run}')
	match args.type:
		case 'basic':
			basic_performance(command_to_run)
		case 'extended':
			extended_performance(command_to_run)
		case _:
			print(f'Unknown type: {args.type}')
