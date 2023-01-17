import numpy as np
import pandas as pd
import os
import re
import csv


abnormal_data_path = "A_TXT/"
normal_data_path = "N_TXT/"
normal_files_paths = [normal_data_path+name for name in os.listdir(normal_data_path) if name]
abnormal_files_paths = [abnormal_data_path+name for name in os.listdir(abnormal_data_path) if name]

csv_file_name = "dataset/lower_limb_emg.csv"


def prepare_dataset_from_folder(csv_file_name, file_paths, class_name):
    count = 0
    with open(csv_file_name, "a+", newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        if not csv_file.read(1):
            csv_writer.writerow(('RF', 'BF', 'VM', 'ST', 'target'))

        for file_path in file_paths:
            add_data_from_txt_to_csv(file_path, csv_writer, class_name, count)


def add_data_from_txt_to_csv(file_path, csv_writer, class_name, count):

    # if count >= 50000:
    #     return
    with open(file_path, 'r') as f:
        for i in range(0, 7):
            next(f)

        stripped_lines = (line.strip() for i, line in enumerate(f) if len(line.split()) != 1 and i < 3000)

        lines = None
        #stripped_lines = (line.strip() for i, line in enumerate(f) if len(line.split()) != 1)
        if class_name is not None:
            lines = (tuple(map(float, re.findall(r'\S+', line)))[0:4]+(class_name, ) for line in stripped_lines if line)
        else:
            lines = (tuple(map(float, re.findall(r'\S+', line)))[0:4] for line in stripped_lines if line)

        csv_writer.writerows(lines)


def load_lower_limb_txt(_filepath ,csv_writer, class_name):
    with open(_filepath) as fp:
        lines = fp.readlines()
        final_lines = tuple()
        for line in lines[7:]:  # first few lines are data description
            items = tuple((float(e) for e in line.split('\t')[:4] if e != ''))+(class_name, )  # last column is not EMG data
            if len(items) != 4:  # last few rows might not have EMG data
                break
            final_lines = final_lines + (items, )
        csv_writer.writerows(final_lines)




if __name__ == "__main__":
    prepare_dataset_from_folder(csv_file_name, normal_files_paths, None)
    #prepare_dataset_from_folder(csv_file_name, abnormal_files_paths, "abnormal")
