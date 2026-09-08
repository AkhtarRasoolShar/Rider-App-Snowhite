with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

imports = """
import androidx.activity.compose.setContent
import androidx.navigation.compose.composable
import androidx.compose.ui.Modifier
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.background
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.foundation.clickable
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material.icons.automirrored.filled.*
import androidx.compose.ui.layout.ContentScale
import coil.compose.AsyncImage
import androidx.navigation.compose.rememberNavController
import androidx.navigation.compose.NavHost
"""

content = content.replace("package com.example", "package com.example\n" + imports)

# Remove the broken fully qualified modifiers I added previously in QuickRepliesScreen
content = content.replace("androidx.compose.ui.Modifier.", "Modifier.")
content = content.replace("androidx.compose.foundation.layout.Box", "Box")
content = content.replace("androidx.compose.foundation.layout.Column", "Column")
content = content.replace("androidx.compose.foundation.layout.Spacer", "Spacer")
content = content.replace("androidx.compose.material3.Text", "Text")
content = content.replace("androidx.compose.material3.OutlinedTextField", "OutlinedTextField")
content = content.replace("androidx.compose.material3.Button", "Button")
content = content.replace("androidx.compose.material3.ButtonDefaults.buttonColors", "ButtonDefaults.buttonColors")
content = content.replace("androidx.compose.foundation.shape.RoundedCornerShape", "RoundedCornerShape")
content = content.replace("androidx.compose.ui.platform.LocalContext.current", "LocalContext.current")

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
