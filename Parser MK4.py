import json
import os
from glob import glob
import csv
import xlsxwriter

# Fields to extract
fields = [
    "@collect.id", "#repo", "@collect.source_name", "@timezone", 
    "#humioAutoShard", "@collect.timestamp", "@rawstring", "@id", 
    "@timestamp", "@ingesttimestamp", "@collect.timezone", "#type", 
    "@collect.host", "@timestamp.nanos", "@collect.file"
]

# Store rows here
all_rows = []

# Read and parse all JSON files
for filename in glob("*.json"):
    print(f"📂 Processing {filename}...")
    with open(filename, "r", encoding="utf-8") as infile:
        for line_num, line in enumerate(infile, start=1):
            try:
                entry = json.loads(line.strip())
                row = [entry.get(key, "") for key in fields]
                all_rows.append(row)
            except json.JSONDecodeError as e:
                print(f"⚠️ Skipping invalid JSON in {filename} at line {line_num}: {e}")

# Save as .xlsx using xlsxwriter
workbook = xlsxwriter.Workbook("CHANGEME.xlsx")
worksheet = workbook.add_worksheet("Logs")

# Write header
for col_num, header in enumerate(fields):
    worksheet.write(0, col_num, header)

# Write data rows
for row_num, row in enumerate(all_rows, start=1):
    for col_num, value in enumerate(row):
        worksheet.write(row_num, col_num, value)

workbook.close()
print("✅ Saved Excel file: CHANGEME.xlsx")

# Save as semicolon-delimited CSV
with open("CHANGEME.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow(fields)
    writer.writerows(all_rows)

print("✅ Saved semicolon CSV file: CHANGEME.csv")
