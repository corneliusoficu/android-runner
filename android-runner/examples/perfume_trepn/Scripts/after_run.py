# noinspection PyUnusedLocal
import subprocess, os
charlesPort = 8888

def restart_charles():
    lsof = subprocess.Popen(['lsof' ,'-n', '-i', '-P'], stdout=subprocess.PIPE)
    grep_listen = subprocess.Popen(['grep', 'LISTEN'], stdin=lsof.stdout, stdout=subprocess.PIPE)
    grep_port = subprocess.Popen(['grep', str(charlesPort)], stdin=grep_listen.stdout, stdout=subprocess.PIPE)
    lsof.stdout.close()
    grep_listen.stdout.close()

    output, error = grep_port.communicate()
    for line in output.splitlines():
        if str(charlesPort) in str(line):
            pid = int(line.split(None, 2)[1])
            print(pid)
            print("Restarting charles with pid: {}".format(pid))
            os.kill(pid,9)

    print("Starting charles")
    subprocess.Popen(['charles', '-throttling', '-headless'])

def main(device, *args, **kwargs):
    device.shell('input tap 600 1000')  # Prevent the device from sleeping
    if kwargs.get('three_g', False):
        restart_charles()

if __name__ == '__main__':
    restart_charles()
