import json

jaw_json_path = "./data/jaw_bottom_1.json"
jaw_csv_path = "./output.csv"

with open(jaw_json_path) as jaw_json_file:
    jaw_json = json.load(jaw_json_file)

    with open(jaw_csv_path, "w") as jaw_csv:
        jaw_csv.write("Frame X Y Probability\n")
        for row in jaw_json:
            a = [1, 2, 3]
            jaw_csv.write(f"{int(row['image'][5:10])} ")
            jaw_csv.write(f"{row['labels']['jaw'][0]} {row['labels']['jaw'][1]} 1.00\n")
        