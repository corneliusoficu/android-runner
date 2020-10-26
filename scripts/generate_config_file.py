import argparse
import csv, json

RANDOMLY_SAMPLED_WEBSITES_CSV = "./RANDOMLY_SAMPLED_WEBSITES.csv"
WEBSITES_FOLDER = "/local_websites"
DEFAULT_WEBSERVER_HOSTNAME = "http://192.168.100.103:9191"
DEFAULT_CONFIG_FILE_LOCATION = "../android-runner/examples/perfume_power/config_web_template.json"


def read_websites_from_csv(csv_file):
    with open(csv_file, "r") as input_csv:
        csv_reader = csv.reader(input_csv, delimiter=",")
        websites = [row[1] for row in csv_reader]
    return websites


def write_config_file(experiment_websites):
    with open(DEFAULT_CONFIG_FILE_LOCATION, "r") as file:
        json_config_template = json.loads(file.read())
        json_config_template["paths"] = experiment_websites

    renamed_config_file = DEFAULT_CONFIG_FILE_LOCATION.replace("_template", "")
    with open(renamed_config_file, "w") as out_file:
        out_file.write(json.dumps(json_config_template, indent=4))


def generate_config_file(file_location=RANDOMLY_SAMPLED_WEBSITES_CSV, local_address=DEFAULT_WEBSERVER_HOSTNAME):
    randomly_sampled_websites = read_websites_from_csv(file_location)
    local_websites_location = [local_address + WEBSITES_FOLDER + "/" + item for item in randomly_sampled_websites]
    write_config_file(local_websites_location)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Pull a host locally')
    parser.add_argument('-i', '--local-address', type=str,
                        help='Local ip address', dest='local_address', required=True)

    parser.add_argument('-f', '--input_csv', type=str,
                        help='Randomly sampled csv list', dest='file_name', required=True)

    args = parser.parse_args()
    generate_config_file(args.file_name, args.local_address)
