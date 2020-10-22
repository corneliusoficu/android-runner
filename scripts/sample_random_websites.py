#!/usr/bin/env python

import argparse
import csv
import random
import urllib.request

DEFAULT_WEBSITES_LIST_LOCATION = "../tranco/top-1m.csv"
DEFAULT_OUTPUT_FILE_NAME = "./RANDOMLY_SAMPLED_WEBSITES.csv"

def format_website_name(website):
	if website.startswith("www."):
		return website

	return "www." + website

def pick_random_website_from_list(websites_list, count_items=30):
	random_indices = []
	for _ in range(0, count_items):
		found_website = False
		while not found_website:
			try:
				random_integer = random.randint(0, len(websites_list)-1)
				if random_integer in random_indices:
					continue
				website = websites_list[random_integer]
				print("Checking valid website: %s" % website)
				code = urllib.request.urlopen("http://"+website, timeout=5).getcode()
				if code == 200:
					random_indices.append(random_integer)
					found_website = True
			except Exception as e:
				print(e)

	return [(index, websites_list[index]) for index in random_indices]


def choose_random_number_of_websites_from_csv_list(input_file=DEFAULT_WEBSITES_LIST_LOCATION,
												   sublist_count=None,
												   num_websites=30,
												   output_file=False):

	with open(input_file, "r") as csv_file_list:
		csv_reader = csv.reader(csv_file_list, delimiter=",")
		all_websites = [format_website_name(item[1]) for item in csv_reader]
		print("Total number of websites: %d" % len(all_websites))

		if sublist_count:
			all_websites = all_websites[:sublist_count]
			print("Total number of websites after sublist prefiltering: %d" % len(all_websites))

		print("Total number of websites to sample: %d" % num_websites)
		randomly_chosen_websites = pick_random_website_from_list(all_websites, num_websites)
		print("Randomly chosen the following %d websites:" % num_websites)

		for index in range(0, len(randomly_chosen_websites)):
			print("%d: %d,%s" % (index + 1, randomly_chosen_websites[index][0], randomly_chosen_websites[index][1]))

	with open(output_file, "w") as out:
		print("Writing to output file: %s" % output_file)
		csv_writer = csv.writer(out)
		csv_writer.writerows([[row[0], row[1]] for row in randomly_chosen_websites])

	return randomly_chosen_websites


def parse_arguments():
	parser = argparse.ArgumentParser(description='Choose a valid number of websites from a csv file')

	parser.add_argument('-i', '--input', type=str, help='CSV containing a list of websites as input', dest='input_file',
						default=DEFAULT_WEBSITES_LIST_LOCATION)

	parser.add_argument('-o', '--output', type=str,
						help="CSV output location for the list of randomly sampled websites", dest='output_file',
						default=DEFAULT_OUTPUT_FILE_NAME)

	parser.add_argument('-s', '--sublist', type=int,
						help="A number representing a sublist from the original list that can be prefiltered",
						dest='sublist_count', default=None)

	parser.add_argument('-n', '--number', type=int,  help="Total number of websites to be sampled",
						dest='count_websites', default=30)

	return parser.parse_args()


if __name__ == '__main__':
	args = parse_arguments()
	choose_random_number_of_websites_from_csv_list(input_file=args.input_file,
												   output_file=args.output_file,
												   sublist_count=args.sublist_count,
												   num_websites=args.count_websites)

