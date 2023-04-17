# Open the input file and read the lines
with open("summary.md", "r") as f:
    lines = f.readlines()

# Split the lines into chunks of 10
chunks = [lines[i : i + 10] for i in range(0, len(lines), 10)]

# Add the footer text to a string
footer = "\ncan you please summarize this, i want to make a github documentation about farcaster, please pull out the relevant information and present it well"

# Write each chunk to a separate output file, feed it to GPT-4
for i, chunk in enumerate(chunks):
    with open(f"asdf_{i+1}.md", "w") as f:
        f.writelines(chunk)
        f.write(footer)
