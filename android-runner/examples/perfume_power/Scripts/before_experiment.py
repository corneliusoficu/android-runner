# noinspection PyUnusedLocal
import subprocess
import time

def start_charles():
    print("Starting Charles")
    subprocess.Popen(['charles', '-throttling', '-headless'])
    print("Sleeping 15 seconds to wait for charles to start")
    time.sleep(15)
    print("Resuming after Charles started")

def main(device, *args, **kwargs):
    if kwargs.get("three_g", False):
        start_charles()

