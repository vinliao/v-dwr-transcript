import subprocess

links = [
    "https://youtube.com/watch?v=nXsgSaM_vE8",
    "https://youtube.com/watch?v=4YGu0T2tGT8",
    "https://youtube.com/watch?v=nGDIdbdtdjE",
    "https://youtube.com/watch?v=zAaKwu-G4DM",
    "https://youtube.com/watch?v=eGafcKj_Qac",
    "https://youtube.com/watch?v=_kdjry8w0dA",
    "https://youtube.com/watch?v=LkpDHdn9GJY",
    "https://youtube.com/watch?v=fW9-dEOSX8A",
    "https://youtube.com/watch?v=tUceJ4n2UIw",
    "https://youtube.com/watch?v=F3bbrFesZDo",
    "https://youtube.com/watch?v=U2b35wbfabI",
    "https://youtube.com/watch?v=Hdy9UEqL9nw",
    "https://youtube.com/watch?v=Nug2zLP8GpI",
    "https://youtube.com/playlist?list=PL0eq1PLf6eUdm35v_840EGLXkVJDhxhcF",
]

# Run a command without capturing its output
for link in links:
    command = f"yt-dlp -x --audio-format mp3 {link}"
    subprocess.call(command, shell=True)
