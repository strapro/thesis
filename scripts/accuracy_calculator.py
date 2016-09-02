import csv
import os
from sklearn.metrics import precision_recall_fscore_support

originalOrParse = raw_input("Do you want to check the [o]riginal or the [p]arsed files?")

if originalOrParse == 'o':
    targetDirectory = 'splitted_files'
else:
    targetDirectoryCandidates = []
    i = 0
    for parsedDirectory in next(os.walk('splitted_parsed_files'))[1]:
        print "["+str(i)+"] "+parsedDirectory
        i += 1
        targetDirectoryCandidates.append(parsedDirectory)
    targetDirectoryCandidateIndex = raw_input("Which parsed files?")
    targetDirectory = 'splitted_parsed_files/'+targetDirectoryCandidates[int(targetDirectoryCandidateIndex)]

y_true = []
y_pred = []
with open(targetDirectory+'/results.csv', 'r') as f:
    next(f)
    reader = csv.reader(f, delimiter=';')
    for row_number, actual_result, ferret_result, coefficient in reader:
        actual_result_label = 'true' if actual_result == '1' else 'false'
        ferret_result_label = 'true' if ferret_result == '1' else 'false'
        y_true.append(actual_result_label)
        y_pred.append(ferret_result_label)

result = precision_recall_fscore_support(y_true, y_pred, average='binary', pos_label=None)
print(result)