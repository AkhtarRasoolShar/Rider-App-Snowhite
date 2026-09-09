import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    code = f.read()

# 1. Update data class Hub
code = re.sub(
    r'data class Hub\(\s*@SerializedName\("id"\) val id: Int\? = null,\s*@SerializedName\("name"\) val name: String\? = null\s*\)',
    r'data class Hub(val id: Int, val name: String)',
    code
)

# 2. Update ViewModel properties
code = code.replace(
    'var availableHubs by androidx.compose.runtime.mutableStateOf<List<Hub>>(emptyList())',
    'val availableHubs = kotlinx.coroutines.flow.MutableStateFlow<List<Hub>>(emptyList())'
)
code = code.replace(
    'var selectedHubs by androidx.compose.runtime.mutableStateOf<Set<String>>(emptySet())',
    'val selectedHubs = androidx.compose.runtime.mutableStateListOf<String>()'
)

# 3. Update fetchAvailableHubs
code = code.replace('availableHubs = body.data', 'availableHubs.value = body.data')

# Remove fallback
fallback_pattern = r'// Fallback in case of HTTP 500 or Network Error\s*availableHubs = listOf\(\s*Hub\(1, "Clifton"\),\s*Hub\(2, "Tariq Road"\),\s*Hub\(3, "DHA Phase 5"\),\s*Hub\(4, "Gulshan-e-Iqbal"\)\s*\)'
code = re.sub(fallback_pattern, '// Fallback removed as requested\n                availableHubs.value = emptyList()', code)

# 4. Update RegisterScreen
code = code.replace(
    'val context = LocalContext.current\n    var name by remember',
    'val context = LocalContext.current\n    val availableHubs by viewModel.availableHubs.collectAsState()\n    var name by remember'
)

old_loop = '''                        viewModel.availableHubs.forEach { hub ->
                            val hubName = hub.name ?: "Unknown"
                            Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth()) {
                                Checkbox(
                                    checked = viewModel.selectedHubs.contains(hubName),
                                    onCheckedChange = { isChecked ->
                                        viewModel.selectedHubs = if (isChecked) viewModel.selectedHubs + hubName else viewModel.selectedHubs - hubName
                                        viewModel.errorMessage = null
                                    },
                                    colors = CheckboxDefaults.colors(checkedColor = TealAccent)
                                )
                                Text(hubName, color = DarkBlue)
                            }
                        }'''

new_loop = '''                        availableHubs.forEach { hub ->
                            val hubName = hub.name
                            Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth()) {
                                Checkbox(
                                    checked = viewModel.selectedHubs.contains(hubName),
                                    onCheckedChange = { isChecked ->
                                        if (isChecked) {
                                            if (!viewModel.selectedHubs.contains(hubName)) viewModel.selectedHubs.add(hubName)
                                        } else {
                                            viewModel.selectedHubs.remove(hubName)
                                        }
                                        viewModel.errorMessage = null
                                    },
                                    colors = CheckboxDefaults.colors(checkedColor = TealAccent)
                                )
                                Text(hubName, color = DarkBlue)
                            }
                        }'''

code = code.replace(old_loop, new_loop)

# Finally, save
with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(code)
