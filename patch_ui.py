import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# LoginScreen
old_login_screen = """fun LoginScreen(viewModel: RiderViewModel, navController: NavController, onNavigateToRegister: () -> Unit, onNavigateToForgotPassword: () -> Unit = {}) {
    val context = LocalContext.current
    var phone by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    val isLoading by viewModel.isLoading.collectAsState()
    val authError by viewModel.authError.collectAsState()"""

new_login_screen = """fun LoginScreen(viewModel: RiderViewModel, navController: NavController, onNavigateToRegister: () -> Unit, onNavigateToForgotPassword: () -> Unit = {}) {
    val context = LocalContext.current
    var email by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    val isLoading by viewModel.isLoading.collectAsState()
    val authError by viewModel.authError.collectAsState()"""
content = content.replace(old_login_screen, new_login_screen)

old_login_fields = """                    OutlinedTextField(
                        value = phone,
                        onValueChange = { phone = it; viewModel.clearError() },
                        label = { Text("Phone Number") },
                        modifier = Modifier.fillMaxWidth(),
                        singleLine = true
                    )"""
new_login_fields = """                    OutlinedTextField(
                        value = email,
                        onValueChange = { email = it; viewModel.clearError() },
                        label = { Text("Email Address") },
                        keyboardOptions = androidx.compose.foundation.text.KeyboardOptions(keyboardType = androidx.compose.ui.text.input.KeyboardType.Email),
                        modifier = Modifier.fillMaxWidth(),
                        singleLine = true
                    )"""
content = content.replace(old_login_fields, new_login_fields)

content = content.replace(
    'viewModel.login(phone, password, context, onSuccess = { navController.navigate("dashboard") { popUpTo(0) } })',
    'viewModel.login(email, password, context, onSuccess = { navController.navigate("dashboard") { popUpTo(0) } })'
)
content = content.replace(
    'enabled = !isLoading && phone.isNotBlank() && password.isNotBlank()',
    'enabled = !isLoading && email.isNotBlank() && password.isNotBlank()'
)

# RegisterScreen
old_register_btn = """                        Button(
                            onClick = {
                                if (isFormValid) {
                                    viewModel.register(name, phone, password, viewModel.selectedHubs.toList(), viewModel.email, context)
                                } else {
                                    android.widget.Toast.makeText(context, "Please fill all fields and select at least one hub.", android.widget.Toast.LENGTH_SHORT).show()
                                }
                            },"""
new_register_btn = """                        Button(
                            onClick = {
                                if (isFormValid) {
                                    viewModel.register(name, phone, password, viewModel.selectedHubs.toList(), viewModel.email, context) {
                                        android.widget.Toast.makeText(context, "Registration successful. Please wait for Admin approval.", android.widget.Toast.LENGTH_LONG).show()
                                        onNavigateToLogin()
                                    }
                                } else {
                                    android.widget.Toast.makeText(context, "Please fill all fields and select at least one hub.", android.widget.Toast.LENGTH_SHORT).show()
                                }
                            },"""
content = content.replace(old_register_btn, new_register_btn)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
