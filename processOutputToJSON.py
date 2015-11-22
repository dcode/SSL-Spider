import csv, json

def readOutput(file):
    datadict = defaultdict(dict)
    urls = []
    
    with open(file, 'rb') as datasetfile:
        dataset = csv.reader(datasetfile)
        for instance in dataset:
            urls.append(instance[1])

    return urls

