import pdfplumber
import pandas as pd
import random

data = []

courses = ["BTech-CSE", "BTech-AIML", "BTech-DS", "BTech-ECE", "BCA", "BSc"]

with pdfplumber.open("details.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()

        if not text:
            continue

        lines = text.split("\n")

        for line in lines:
            parts = line.strip().split()

            # Skip invalid lines
            if len(parts) < 2:
                continue

            enrollment = parts[0]

            # IMPORTANT: your enrollment contains letters → just check starts with 2
            if not enrollment.startswith("2"):
                continue

            name = " ".join(parts[1:])

            # Random phone
            phone = str(random.randint(6000000000, 9999999999))

            # Random course
            course = random.choice(courses)

            data.append((enrollment, name, phone, course))

# ✅ REMOVE DUPLICATES (based on enrollment)
unique_data = {}
for row in data:
    unique_data[row[0]] = row

final_data = list(unique_data.values())

# Create DataFrame
df = pd.DataFrame(final_data, columns=["enrollment", "name", "phone", "course"])

# Sort for clean output
df = df.sort_values(by="enrollment")

# Save CSV
df.to_csv("students_full.csv", index=False)

print(f"✅ CSV created successfully with {len(df)} students!")