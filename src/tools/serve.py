import subprocess

def run():
	print('[open]http://localhost:8000')
	subprocess.run(["python", "-m", "http.server", "8000"])
	