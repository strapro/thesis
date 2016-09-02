import csv
import os

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

threshold = float(input('What\'s the threshold? > '))
result_file = open(targetDirectory+'/results.csv', 'w')
result_file.truncate()
result_file_writer = csv.writer(result_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
result_file_writer.writerow([
    'Row #',
    'Actual Result',
    'Ferret Result (threshold = ' + str(threshold) + ')',
    'Jaccard Coefficient'
])
i = 0
with open('MSRParaphraseCorpus/msr_paraphrase_train.txt', 'r') as f:
    next(f)  # skip headers
    reader = csv.reader(f, delimiter='\t')
    for result, id1, id2, string1, string2 in reader:
        i += 1
        with open(targetDirectory+'/'+str(i) + '/ferret_result.txt', 'r') as ferret_output:
            ferret_output_reader = csv.reader(ferret_output, delimiter=';')
            ferret_result_row = next((x for j, x in enumerate(ferret_output_reader) if j == 2), None)
            ferret_jaccard_coefficient = ferret_result_row[5].strip()
            result_file_writer.writerow([
                str(i),
                result,
                1 if float(ferret_jaccard_coefficient) > threshold else 0,
                ferret_jaccard_coefficient,
            ])

result_file.close()
