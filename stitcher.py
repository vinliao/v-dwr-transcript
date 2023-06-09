import os
import re

transcript_dir = "transcript"
txt_files = sorted(
    [file for file in os.listdir(transcript_dir) if file.endswith(".txt")]
)

title_pattern = re.compile(r"(?<=\[).+?(?=\])")
merged_files = {}
for file in txt_files:
    title_match = title_pattern.search(file)
    if title_match:
        title = title_match.group()
        with open(os.path.join(transcript_dir, file), "r") as f:
            content = f.read()
        if "_part" not in file:
            merged_files[title] = content
        else:
            if title in merged_files:
                merged_files[title] += content
            else:
                merged_files[title] = content

with open("rawall.md", "w") as outfile:
    for filename in sorted(os.listdir(transcript_dir)):
        if filename.endswith(".txt") and not filename.startswith("all"):
            # Get the base name without extension
            title = os.path.splitext(filename)[0]

            with open(os.path.join(transcript_dir, filename), "r") as infile:
                content = infile.read()

                outfile.write(f"# {title}\n\n")
                outfile.write(content)
                outfile.write("\n\n")

print("File 'rawall.md' has been generated.")
