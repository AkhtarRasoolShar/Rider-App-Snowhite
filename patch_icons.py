import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Fix Icon issue by changing Icons.AutoMirrored.Filled.ListAlt to a standard icon like Icons.Default.List or simply Icons.Default.Menu to ensure compilation
content = content.replace("Icons.AutoMirrored.Filled.ListAlt", "Icons.Default.Menu")

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
