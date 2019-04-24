import os

import numpy
import pandas as pd
from pm4py.objects.log.exporter.csv import factory as csv_exporter
from pm4py.objects.log.importer.xes import factory as xes_importer


def convert_to_csv(xes_path, csv_path):
    log = xes_importer.apply(xes_path)
    csv_exporter.export(log, csv_path)
    alignment = pd.read_csv(csv_path)
    os.remove(csv_path)
    alignment = alignment.dropna(subset=["case Company"])
    alignment.to_csv(f"{csv_path}.gz")
