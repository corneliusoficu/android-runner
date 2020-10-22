import csv, os, sys
from collections import OrderedDict
from functools import reduce


def write_to_file(filename, rows):
    with open(filename, 'w') as f:
        writer = csv.DictWriter(f, list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def list_subdir(a_dir):
    """List immediate subdirectories of a_dir"""
    # https://stackoverflow.com/a/800201
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


def aggregate_final(data_dir):
    rows = []
    for device in list_subdir(data_dir):
        row = OrderedDict({'device': device})
        device_dir = os.path.join(data_dir, device)
        for subject in list_subdir(device_dir):
            row.update({'subject': subject})
            subject_dir = os.path.join(device_dir, subject)
            if os.path.isdir(os.path.join(subject_dir, 'batterystats')):
                row.update(aggregate_battery_final(os.path.join(subject_dir, 'batterystats')))
                rows.append(row.copy())
            else:
                for browser in list_subdir(subject_dir):
                    row.update({'browser': browser})
                    browser_dir = os.path.join(subject_dir, browser)
                    if os.path.isdir(os.path.join(browser_dir, 'batterystats')):
                        row.update(aggregate_battery_final(os.path.join(browser_dir, 'batterystats')))
                        rows.append(row.copy())
    return rows


def aggregate_battery_subject(logs_dir, joules):
    def add_row(accum, new):
        row = {k: v + float(new[k]) for k, v in list(accum.items()) if k not in ['Component', 'count']}
        count = accum['count'] + 1
        return dict(row, **{'count': count})

    # FIX
    runs = []
    runs_total = dict()
    for run_file in [f for f in os.listdir(logs_dir) if os.path.isfile(os.path.join(logs_dir, f))]:
        if ('Joule' in run_file) and joules:
            with open(os.path.join(logs_dir, run_file), 'r', encoding='utf-8') as run:
                reader = csv.DictReader(run)
                init = dict({fn: 0 for fn in reader.fieldnames if fn != 'datetime'}, **{'count': 0})
                run_total = reduce(add_row, reader, init)
                runs.append({k: v / run_total['count'] for k, v in list(run_total.items()) if k != 'count'})
            runs_total = reduce(lambda x, y: {k: v + y[k] for k, v in list(x.items())}, runs)
    return OrderedDict(
        sorted(list({'batterystats_' + k: v / len(runs) for k, v in list(runs_total.items())}.items()),
               key=lambda x: x[0]))


def aggregate_battery_final(logs_dir):
    for aggregated_file in [f for f in os.listdir(logs_dir) if os.path.isfile(os.path.join(logs_dir, f))]:
        if aggregated_file == "Aggregated.csv":
            with open(os.path.join(logs_dir, aggregated_file), 'r', encoding='utf-8') as aggregated:
                reader = csv.DictReader(aggregated)
                row_dict = OrderedDict()
                for row in reader:
                    for f in reader.fieldnames:
                        row_dict.update({f: row[f]})
                return OrderedDict(row_dict)


def aggregate_end(data_dir, output_file):
    rows = aggregate_final(data_dir)
    write_to_file(output_file, rows)


if __name__ == '__main__':
    data_dir = sys.argv[1]
    output_file = sys.argv[2]
    aggregate_end(data_dir, output_file)