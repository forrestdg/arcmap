import sys, os, csv, pprint

def main():
    if sys.argv[1:]:
        input_file = sys.argv[1]
    else:
        input_file = "Data_name_convention.csv"

    reader = csv.reader(open(input_file))

    data_path   = os.path.join(dirname, "..", "Data")
    result_path   = os.path.join(dirname, "..", "Data", "result")

    if os.path.exists(result_path):
        raise Exception("%s exists. Remove it manually before proceding"
                        %result_path)


    col_map = {}
    configs = {}
    for i,row in enumerate(reader):
        if i == 0:
            for j,word in enumerate(row):
                col_map[j] = word
                configs[word] = []
        else:
            for j,word in enumerate(row):
                key = col_map[j]
                configs[key].append(word)

    print pprint.pprint(configs)

if __name__ == '__main__':
    main()
