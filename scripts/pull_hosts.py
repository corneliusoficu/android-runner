import argparse
import csv
import os
import shutil
import subprocess

from multiprocessing import Pool

MULTIPROCESSING_PARALLELISM = 8

def pull_and_store_host_locally(website_dict):
    hostname = website_dict['website']
    location = website_dict['destination']
    subprocess.run(["wget", "--page-requisites", "--convert-links", "-P", location, hostname])
    print("Stored " + hostname + " to " + location)

def delete_folder_contents(folder_location):
    for filename in os.listdir(folder_location):
        file_path = os.path.join(folder_location, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def read_randomly_sampled_websites_list(file_location):
    with open(file_location, "r") as in_file:
        csv_reader = csv.reader(in_file)
        websites = [row[1] for row in csv_reader]
    return websites

def pull_list_of_websites_locally(websites_list, destination_folder):
    if not os.path.isdir(destination_folder):
        os.mkdir(destination_folder)
    else:
        delete_folder_contents(destination_folder)

    websites_list = [{"website": website, "destination": destination_folder} for website in websites_list]
    print(websites_list)

    with Pool(MULTIPROCESSING_PARALLELISM) as p:
        p.map(pull_and_store_host_locally, websites_list)


def pull_websites_from_csv(input_file, destination_folder):
    randomly_sampled_websites = read_randomly_sampled_websites_list(input_file)
    pull_list_of_websites_locally(randomly_sampled_websites, destination_folder)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Pull a host locally')
    parser.add_argument('-w', '--webpage', type=str,
                        help='Hostname to be pulled locally', dest='hostname', default=None)

    parser.add_argument('-f', '--folder', type=str, required=True,
                        help="Location where to store the local folder", dest='folder')

    parser.add_argument('-i', '--input', type=str, dest='hostnames',
                        help="Input csv with sampled websites to download", default=None)

    args = parser.parse_args()

    if not args.hostnames and args.hostname:
        data = {
            'website': args.hostname,
            'destination': args.folder
        }
        pull_and_store_host_locally(data)
    elif args.hostnames:
        pull_websites_from_csv(args.hostnames, args.folder)
    elif not args.hostnames and not args.hostname:
        print("Error: No website to pull")
