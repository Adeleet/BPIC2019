from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.objects.log.exporter.csv import factory as csv_exporter


def xes_to_csv(xes_path, csv_path):
    """
    Imports .xes given the xes_path, and converts and saves it to a .csv file
    Args:
        xes_path (str) : path of .xes compliant input event log
        csv_path (str) : path of .csv output event log
    """
    log = xes_import_factory.apply(xes_path)
    csv_exporter.export(log, csv_path)
