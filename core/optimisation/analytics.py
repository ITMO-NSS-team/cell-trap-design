import csv
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


class EvoAnalytics:
    run_id = 'def'

    @staticmethod
    def save_cantidate(pop_num, objectives, anlytics_objectives, genotype, referenced_dataset, local_id,
                       subfolder_name=None):

        if not os.path.isdir(f'HistoryFiles'):
            os.mkdir(f'HistoryFiles')

        if subfolder_name:
            if not os.path.isdir(f'HistoryFiles/{subfolder_name}'):
                os.mkdir(f'HistoryFiles/{subfolder_name}')

            hist_file_name = f'HistoryFiles/{subfolder_name}/history_{EvoAnalytics.run_id}.csv'

        else:
            hist_file_name = f'HistoryFiles/history_{EvoAnalytics.run_id}.csv'
        if not os.path.isfile(hist_file_name):
            with open(hist_file_name, 'w', newline='') as f:
                EvoAnalytics._write_header_to_csv(f, objectives, anlytics_objectives, genotype)
                EvoAnalytics._write_candidate_to_csv(f, pop_num, objectives, anlytics_objectives, genotype,
                                                     referenced_dataset, local_id)
        else:
            with open(hist_file_name, 'a', newline='') as f:
                EvoAnalytics._write_candidate_to_csv(f, pop_num, objectives, anlytics_objectives, genotype,
                                                     referenced_dataset, local_id)

    @staticmethod
    def _write_candidate_to_csv(f, pop_num, objs, analytics_objectives, genotype, referenced_dataset, local_id):
        writer = csv.writer(f, delimiter=',', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(
            [pop_num, referenced_dataset, ','.join([str(round(_, 6)) for _ in objs]),
             analytics_objectives, local_id])

    @staticmethod
    def _write_header_to_csv(f, objectives, analytics_objectives, genotype):
        if len(analytics_objectives) == 0:
            analytics_objectives = []
        writer = csv.writer(f, delimiter=',', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(
            ['pop_num', 'referenced_dataset', ','.join([f'obj{_}' for _ in range(0, len(objectives))]),
             ','.join([f'ananlytics_ob{_}' for _ in range(len(analytics_objectives))]), 'local_id'])

    @staticmethod
    def clear():
        hist_file_name = f'HistoryFiles/history_{EvoAnalytics.run_id}.csv'
        if os.path.isfile(hist_file_name):
            os.remove(hist_file_name)

    @staticmethod
    def create_boxplot():
        f = f'HistoryFiles/history_{EvoAnalytics.run_id}.csv'

        df = pd.read_csv(f, header=0, sep="\s*,\s*")
        df['obj0'] = -df['obj0']

        df = df.loc[df['pop_num'] % 2 == 0]

        plt.clf()
        plt.figure(figsize=(20, 10))
        # plt.xticks(rotation=45)

        fsize = 24
        plt.rcParams["font.size"] = fsize
        plt.tick_params(labelsize=fsize)
        plt.rc('xtick', labelsize=fsize)
        plt.rc('ytick', labelsize=fsize)
        plt.xticks(rotation=90)
        plt.yticks(rotation=90)

        sns.boxplot(x=df['pop_num'], y=df['obj0'], palette="Blues")

        plt.ylabel('Fitness (flow ratio)', fontsize=fsize)
        plt.xlabel('Generations, #', fontsize=fsize, rotation=180)

        plt.hlines(y=max(df['obj0']), xmin=min(df['pop_num']), xmax=max(df['pop_num']),
                   linestyles='dashed')

        plt.text(min(df['obj0']), max(df['obj0']) * 0.97,
                 f"Best found topology with fitness {round(max(df['obj0']), 4)}",
                 size=fsize, rotation=180)

        ax = plt.gca()
        for index, label in enumerate(ax.xaxis.get_ticklabels()):
            if index % 10 != 0:
                label.set_visible(False)

        # plt.show()
        plt.savefig('D://fitness.png', dpi=300)

        if 'obj1' in df.columns:
            plt.figure(figsize=(20, 10))
            plt.xticks(rotation=45)
            sns.boxplot(x=df['pop_num'], y=df['obj1'], palette="Blues")
            plt.show()
