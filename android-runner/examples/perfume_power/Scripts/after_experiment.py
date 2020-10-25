# noinspection PyUnusedLocal
import subprocess, os
charlesPort = 8888

def close_charles():
    lsof = subprocess.Popen(['lsof', '-n', '-i', '-P'], stdout=subprocess.PIPE)
    grep_listen = subprocess.Popen(['grep', 'LISTEN'], stdin=lsof.stdout, stdout=subprocess.PIPE)
    grep_port = subprocess.Popen(['grep', str(charlesPort)], stdin=grep_listen.stdout, stdout=subprocess.PIPE)
    lsof.stdout.close()
    grep_listen.stdout.close()

    output, error = grep_port.communicate()
    for line in output.splitlines():
        if str(charlesPort) in str(line):
            pid = int(line.split(None, 2)[1])
            print(pid)
            print("Killing charles with pid: {}".format(pid))
            os.kill(pid, 9)

def main(device, *args, **kwargs):
    if kwargs.get("three_g", False):
        close_charles()
