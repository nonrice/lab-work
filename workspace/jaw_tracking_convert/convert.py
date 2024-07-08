import jaw_tracking_convert
import glob

for path in glob.glob("../Licking_Data/Licking_Data/**/*.json", recursive=True):
    print(f"Converting {path}")
    jaw_tracking_convert.json_to_csv(path, path[:-5]+".csv")
    print("Done")
