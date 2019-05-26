import os

from pm4py.objects.log.exporter.csv import factory as csv_exporter
from pm4py.objects.log.importer.xes import factory as xes_import_factory


def xes_to_csv(xes_path, csv_path):
    """
    Imports .xes given the xes_path, and converts and saves it to a .csv file
    Args:
        xes_path (str) : path of .xes compliant input event log
        csv_path (str) : path of .csv output event log
    """
    log = xes_import_factory.apply(xes_path)
    csv_exporter.export(log, csv_path)


b_path = "../Data/Alignments"

xes_files = [f for f in os.listdir(
    f"{b_path}/") if f.find(".xes") > 0]


for xes_fname in xes_files:
    xes_path = f"{b_path}/{xes_fname}"
    csv_path = f"{b_path}/{xes_fname.replace('.xes','.csv')}"
    xes_to_csv(xes_path, csv_path)
