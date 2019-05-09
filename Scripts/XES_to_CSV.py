from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.objects.log.exporter.csv import factory as csv_exporter


categories = ["2-way", "3-way-before-GR", "3-way-after-GR", "consignment"]
alignment_path = "./Data/Alignments"
for cat in categories:
    f_path = f"{alignment_path}/alignment-{cat}.xes"
    print(f_path)
    log = xes_import_factory.apply(f_path)
    csv_exporter.export(log, f"alignment-{cat}.csv")
