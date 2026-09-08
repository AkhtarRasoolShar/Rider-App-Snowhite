with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# 1. MainAppScreen signature
content = content.replace(
    'fun MainAppScreen(viewModel: RiderViewModel) {',
    'fun MainAppScreen(viewModel: RiderViewModel, onLogout: () -> Unit = {}) {'
)

# 2. MainAppScreen invocation in MainActivity
content = content.replace(
    'MainAppScreen(viewModel)',
    'MainAppScreen(viewModel, onLogout = { navController.navigate("auth") { popUpTo(0) } })'
)

# 3. ProfileScreen signature
content = content.replace(
    'fun ProfileScreen(viewModel: RiderViewModel, navController: NavHostController) {',
    'fun ProfileScreen(viewModel: RiderViewModel, navController: NavHostController, onLogout: () -> Unit = {}) {'
)

# 4. ProfileScreen invocation in MainAppScreen
content = content.replace(
    'composable("profile") { ProfileScreen(viewModel, navController) }',
    'composable("profile") { ProfileScreen(viewModel, navController, onLogout) }'
)

# 5. ProfileScreen logout button
old_logout = '''                        SettingsRow(icon = Icons.Default.Logout, text = "Logout", isDestructive = true, onClick = {
                            viewModel.logout(context)
                            navController.navigate("auth") { popUpTo(0) }
                        })'''
new_logout = '''                        SettingsRow(icon = Icons.AutoMirrored.Filled.Logout, text = "Logout", isDestructive = true, onClick = {
                            viewModel.logout(context)
                            onLogout()
                        })'''
content = content.replace(old_logout, new_logout)

# While here, fix the Icons.Filled.Chat deprecation in ProfileScreen
content = content.replace(
    'SettingsRow(icon = Icons.Default.Chat, text = "Manage Quick Replies", onClick = { navController.navigate("quickReplies") })',
    'SettingsRow(icon = Icons.AutoMirrored.Filled.Chat, text = "Manage Quick Replies", onClick = { navController.navigate("quickReplies") })'
)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
