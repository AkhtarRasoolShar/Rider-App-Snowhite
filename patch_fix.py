import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

components = """
@Composable
fun StatItem(icon: androidx.compose.ui.graphics.vector.ImageVector, label: String, value: String) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Icon(icon, contentDescription = null, tint = TealAccent, modifier = Modifier.size(28.dp))
        Spacer(Modifier.height(4.dp))
        Text(value, fontWeight = FontWeight.Bold, fontSize = 18.sp, color = Color(0xFF1E293B))
        Text(label, fontSize = 12.sp, color = Color(0xFF64748B))
    }
}

@Composable
fun SettingsRow(icon: androidx.compose.ui.graphics.vector.ImageVector, text: String, isDestructive: Boolean = false, onClick: () -> Unit) {
    val color = if (isDestructive) ErrorRed else Color(0xFF334155)
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick)
            .padding(16.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(icon, contentDescription = null, tint = color, modifier = Modifier.size(24.dp))
        Spacer(Modifier.width(16.dp))
        Text(text, fontWeight = FontWeight.SemiBold, fontSize = 15.sp, color = color, modifier = Modifier.weight(1f))
        Icon(Icons.Default.ChevronRight, contentDescription = null, tint = Color(0xFF94A3B8), modifier = Modifier.size(20.dp))
    }
}
"""

content = content.replace("@OptIn(ExperimentalMaterial3Api::class)\n@Composable\nfun QuickRepliesScreen", components + "\n@OptIn(ExperimentalMaterial3Api::class)\n@Composable\nfun QuickRepliesScreen")

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
