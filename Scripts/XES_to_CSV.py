from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.objects.log.exporter.csv import factory as csv_exporter


def xes_to_csv(xes_path, csv_path):
    """
    Imports .xes given the xes_path, and converts and saves it to a .csv file
    Args:
        xes_path (str) : path of .xes compliant input event log
        csv_path (str) : path of .csv output event log
    """
    log = xes_import_factory.apply(f_path)
    csv_exporter.export(log, f"alignment-{cat}.csv")


# Using the 4 created alignments for each matching categories, specified in the ALIGNMENTS_PATH
MATCHING_CATEGORIES = ["2-way", "3-way-before-GR",
                       "3-way-after-GR", "consignment"]
ALIGNMENTS_PATH = "./Data/Alignments"

for cat in MATCHING_CATEGORIES:
    xes_to_csv(xes_path=f"{ALIGNMENTS_PATH}/alignment-{cat}.xes",
               csv_path=f"{ALIGNMENTS_PATH}/alignment-{cat}.csv")
