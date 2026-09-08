with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

content = content.replace(
    'Icons.Default.Sort',
    'Icons.AutoMirrored.Filled.Sort'
)
content = content.replace(
    'Icons.Filled.Sort',
    'Icons.AutoMirrored.Filled.Sort'
)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
