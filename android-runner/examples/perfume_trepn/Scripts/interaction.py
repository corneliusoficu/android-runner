# noinspection PyUnusedLocal
import os, sys, time

PERFUME_JS_RESULTS_FOLDER = os.path.join(os.getcwd(), 'output')
SLEEP_DURATION = 0.2

def main(device, *args, **kwargs):
    timeout_duration = kwargs['duration_wait']
    print("Waiting for perfume_js directory to have data")
    start_time = time.time()

    while True:
        time.sleep(SLEEP_DURATION)
        time_passed = time.time() - start_time
        timeout_exceeded = time_passed >= timeout_duration
        does_folder_contain_perfume_results = len(os.listdir(PERFUME_JS_RESULTS_FOLDER)) != 0
        if timeout_exceeded or does_folder_contain_perfume_results:
            break

    if does_folder_contain_perfume_results:
        print("perfume_js directory has data, waiting over")
    if timeout_exceeded:
        print("Timeout of {}s exceeded while waiting for perfume results".format(timeout_duration))





