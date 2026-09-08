with open("app/src/main/java/com/example/RiderUI.kt", "r") as f:
    content = f.read()

imports = """
import coil.compose.AsyncImage
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.draw.clip
import androidx.compose.material.icons.automirrored.filled.Chat
"""

content = content.replace("package com.example", "package com.example\n" + imports)
content = content.replace("Icons.AutoMirrored.Filled.Chat", "Icons.Default.Email")

with open("app/src/main/java/com/example/RiderUI.kt", "w") as f:
    f.write(content)
