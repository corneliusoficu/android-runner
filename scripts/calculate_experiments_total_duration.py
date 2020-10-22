import sys, os, csv, datetime

WAIT_DURATION_EXPERIMENT_SECONDS = 120
TOTAL_DURATION = 0.0
COUNT_EXPERIMENT_SUBJECTS = 0

def extract_experiment_duration_batterystats(batterystats_file_location):
    global TOTAL_DURATION
    global COUNT_EXPERIMENT_SUBJECTS

    with open(batterystats_file_location, newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if not (len(row) >= 4):
                continue
            if row[3] == "screen dark":
                COUNT_EXPERIMENT_SUBJECTS += 1
                TOTAL_DURATION += (float(row[2]) + WAIT_DURATION_EXPERIMENT_SECONDS)

def calculate_all_experiments_execution_time(folder_experiments):
    for dirpath, dirnames, filenames in os.walk(folder_experiments):
        if dirpath.endswith("batterystats"):
            for file in filenames:
                if file.startswith("results_"):
                    complete_path = os.path.join(dirpath, file)
                    extract_experiment_duration_batterystats(complete_path)

    experiment_duration_str = datetime.timedelta(seconds=TOTAL_DURATION)
    print("Total number of subjects = {}".format(COUNT_EXPERIMENT_SUBJECTS))
    print("Total experiments duration = {}".format(experiment_duration_str))

if __name__ == '__main__':
    folder_experiments = sys.argv[1]
    calculate_all_experiments_execution_time(folder_experiments)