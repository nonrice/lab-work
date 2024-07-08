import json

def json_to_csv(jaw_json_path, jaw_csv_path):
    with open(jaw_json_path) as jaw_json_file:
        jaw_json = json.load(jaw_json_file)

        with open(jaw_csv_path, "w") as jaw_csv:
            jaw_csv.write("Frame X Y Probability\n")
            for row in jaw_json:
                if len(row['labels']['jaw']) == 2:
                    jaw_csv.write(f"{int(''.join(filter(str.isdigit, row['image'])))} ")
                    jaw_csv.write(f"{row['labels']['jaw'][1]} {row['labels']['jaw'][0]} 1.00\n")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Convert jaw tracking data from JSON to CSV.")
    parser.add_argument("--in", required=True, help="Input JSON file path")
    parser.add_argument("--out", required=True, help="Output CSV file path")
    args = parser.parse_args()
    json_to_csv(args.input, args.output)
