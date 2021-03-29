from datetime import datetime

# datetime object containing current date and time
now = datetime.now()

now = str(now).split(" ")
key1 = "".join(now[0].split("-"))
key2 = "".join(("".join(now[1].split(":")).split(".")))
key = key2 + key1
print(key)