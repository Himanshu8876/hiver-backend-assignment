import pandas as pd

file_path = r"C:\Users\admin\Desktop\Hiver\archive\twcs\twcs.csv"
output_path = "data/amazon_help.csv"

amazon_rows = []

for chunk in pd.read_csv(file_path, chunksize=100000):
    rows = chunk[chunk["author_id"] == "AmazonHelp"]
    amazon_rows.append(rows)

amazon_data = pd.concat(amazon_rows, ignore_index=True)

print("Total AmazonHelp tweets:", len(amazon_data))

amazon_data.to_csv(output_path, index=False)

print("Saved to:", output_path)