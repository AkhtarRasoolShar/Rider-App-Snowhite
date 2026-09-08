import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# 1. Add Requests
requests = """data class RiderLoginRequest(@SerializedName("phone") val phone: String? = null, val password: String, val is_rider_app: Boolean = true)
data class ForgotPasswordRequest(val email: String)
data class ResetPasswordWithOtpRequest(val email: String, val otp: String, val new_password: String)"""
content = content.replace('data class RiderLoginRequest(@SerializedName("phone") val phone: String? = null, val password: String, val is_rider_app: Boolean = true)', requests)


# 2. Add API Endpoints
api_endpoints = """    @Headers("Content-Type: application/json")
    @POST("routes.php?action=rider_register")
    suspend fun register(@Body request: RiderRegisterRequest): Response<GenericResponse<RiderAuthData>>

    @Headers("Content-Type: application/json")
    @POST("routes.php?action=forgot_password_request")
    suspend fun forgotPassword(@Body request: ForgotPasswordRequest): Response<GenericResponse<Any>>

    @Headers("Content-Type: application/json")
    @POST("routes.php?action=reset_password_with_otp")
    suspend fun resetPassword(@Body request: ResetPasswordWithOtpRequest): Response<GenericResponse<RiderAuthData>>"""
content = content.replace("""    @Headers("Content-Type: application/json")
    @POST("routes.php?action=rider_register")
    suspend fun register(@Body request: RiderRegisterRequest): Response<GenericResponse<RiderAuthData>>""", api_endpoints)


# 3. Add ViewModel & Screen
new_ui_and_vm = """
class RiderForgotPasswordViewModel : ViewModel() {
    var currentStep by androidx.compose.runtime.mutableStateOf(1)
    var email by androidx.compose.runtime.mutableStateOf("")
    var otp by androidx.compose.runtime.mutableStateOf("")
    var newPassword by androidx.compose.runtime.mutableStateOf("")
    
    var isLoading by androidx.compose.runtime.mutableStateOf(false)
    var errorMessage by androidx.compose.runtime.mutableStateOf<String?>(null)
    var successMessage by androidx.compose.runtime.mutableStateOf<String?>(null)

    fun sendOtp() {
        if (email.isBlank()) {
            errorMessage = "Please enter your email"
            return
        }
        isLoading = true
        errorMessage = null
        successMessage = null
        androidx.lifecycle.viewModelScope.launch {
            try {
                val res = RetrofitClient.apiService.forgotPassword(ForgotPasswordRequest(email))
                if (res.isSuccessful && res.body()?.status == "success") {
                    successMessage = res.body()?.message ?: "OTP sent successfully"
                    currentStep = 2
                } else {
                    errorMessage = res.body()?.message ?: "Failed to send OTP"
                }
            } catch (e: Exception) {
                errorMessage = "Network error: ${e.message}"
            } finally {
                isLoading = false
            }
        }
    }

    fun verifyAndReset(context: android.content.Context, onSuccess: () -> Unit) {
        if (otp.isBlank() || newPassword.isBlank()) {
            errorMessage = "Please fill in all fields"
            return
        }
        isLoading = true
        errorMessage = null
        successMessage = null
        androidx.lifecycle.viewModelScope.launch {
            try {
                val res = RetrofitClient.apiService.resetPassword(ResetPasswordWithOtpRequest(email, otp, newPassword))
                if (res.isSuccessful && res.body()?.status == "success") {
                    res.body()?.data?.let {
                        SessionManager.saveUser(context, it)
                        onSuccess()
                    } ?: run {
                        errorMessage = "Invalid response from server"
                    }
                } else {
                    errorMessage = res.body()?.message ?: "Failed to reset password"
                }
            } catch (e: Exception) {
                errorMessage = "Network error: ${e.message}"
            } finally {
                isLoading = false
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun RiderForgotPasswordScreen(onNavigateToLogin: () -> Unit, onNavigateToDashboard: () -> Unit) {
    val viewModel: RiderForgotPasswordViewModel = androidx.lifecycle.viewmodel.compose.viewModel()
    val context = LocalContext.current

    Box(modifier = Modifier.fillMaxSize()) {
        AsyncImage(
            model = "https://images.pexels.com/photos/5591581/pexels-photo-5591581.jpeg?auto=compress&cs=tinysrgb&w=1080",
            contentDescription = "Background",
            contentScale = ContentScale.Crop,
            modifier = Modifier.fillMaxSize()
        )
        Box(modifier = Modifier.fillMaxSize().background(Color.Black.copy(alpha = 0.65f)))
        
        Column(
            modifier = Modifier.fillMaxSize().imePadding().padding(24.dp).verticalScroll(rememberScrollState()),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                Icon(Icons.Default.LockReset, contentDescription = null, modifier = Modifier.size(80.dp), tint = Color.White)
                Spacer(modifier = Modifier.height(8.dp))
                Text(
                    text = "Reset Password",
                    fontSize = 24.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color.White
                )
                Text(
                    text = if (viewModel.currentStep == 1) "Enter your email to receive an OTP" else "Enter OTP and your new password",
                    color = Color.White.copy(alpha = 0.8f),
                    textAlign = androidx.compose.ui.text.style.TextAlign.Center
                )
            }
            Spacer(Modifier.height(32.dp))
            
            Card(
                colors = CardDefaults.cardColors(containerColor = Color.White),
                shape = RoundedCornerShape(24.dp),
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.padding(24.dp)) {
                    viewModel.errorMessage?.let {
                        Text(it, color = ErrorRed, modifier = Modifier.padding(bottom = 8.dp), fontSize = 14.sp)
                    }
                    viewModel.successMessage?.let {
                        Text(it, color = Color(0xFF10B981), modifier = Modifier.padding(bottom = 8.dp), fontSize = 14.sp)
                    }

                    if (viewModel.currentStep == 1) {
                        OutlinedTextField(
                            value = viewModel.email,
                            onValueChange = { viewModel.email = it },
                            label = { Text("Email") },
                            leadingIcon = { Icon(Icons.Default.Email, contentDescription = null, tint = DarkBlue) },
                            modifier = Modifier.fillMaxWidth(),
                            singleLine = true,
                            keyboardOptions = androidx.compose.foundation.text.KeyboardOptions(keyboardType = androidx.compose.ui.text.input.KeyboardType.Email)
                        )
                        Spacer(Modifier.height(24.dp))
                        Button(
                            onClick = { viewModel.sendOtp() },
                            modifier = Modifier.fillMaxWidth().height(50.dp),
                            colors = ButtonDefaults.buttonColors(containerColor = DarkBlue),
                            enabled = !viewModel.isLoading
                        ) {
                            if (viewModel.isLoading) CircularProgressIndicator(color = Color.White, modifier = Modifier.size(24.dp))
                            else Text("SEND OTP", color = Color.White, fontWeight = FontWeight.Bold)
                        }
                    } else {
                        OutlinedTextField(
                            value = viewModel.otp,
                            onValueChange = { viewModel.otp = it },
                            label = { Text("OTP Code") },
                            leadingIcon = { Icon(Icons.Default.VpnKey, contentDescription = null, tint = DarkBlue) },
                            modifier = Modifier.fillMaxWidth(),
                            singleLine = true,
                            keyboardOptions = androidx.compose.foundation.text.KeyboardOptions(keyboardType = androidx.compose.ui.text.input.KeyboardType.Number)
                        )
                        Spacer(Modifier.height(16.dp))
                        OutlinedTextField(
                            value = viewModel.newPassword,
                            onValueChange = { viewModel.newPassword = it },
                            label = { Text("New Password") },
                            leadingIcon = { Icon(Icons.Default.Lock, contentDescription = null, tint = DarkBlue) },
                            modifier = Modifier.fillMaxWidth(),
                            visualTransformation = androidx.compose.ui.text.input.PasswordVisualTransformation(),
                            singleLine = true
                        )
                        Spacer(Modifier.height(24.dp))
                        Button(
                            onClick = { viewModel.verifyAndReset(context, onNavigateToDashboard) },
                            modifier = Modifier.fillMaxWidth().height(50.dp),
                            colors = ButtonDefaults.buttonColors(containerColor = DarkBlue),
                            enabled = !viewModel.isLoading
                        ) {
                            if (viewModel.isLoading) CircularProgressIndicator(color = Color.White, modifier = Modifier.size(24.dp))
                            else Text("VERIFY & RESET", color = Color.White, fontWeight = FontWeight.Bold)
                        }
                    }
                }
            }
            
            Spacer(Modifier.height(24.dp))
            TextButton(onClick = onNavigateToLogin) {
                Text("Back to Login", color = TealAccent, fontWeight = FontWeight.Bold)
            }
        }
    }
}

@Composable
fun AuthFlow(viewModel: RiderViewModel, navController: NavHostController) {"""
content = content.replace("@Composable\nfun AuthFlow(viewModel: RiderViewModel, navController: NavHostController) {", new_ui_and_vm)

# 4. Modify AuthFlow & LoginScreen
old_auth_flow = """@Composable
fun AuthFlow(viewModel: RiderViewModel, navController: NavHostController) {
    var isLogin by remember { mutableStateOf(true) }
    
    if (isLogin) {
        LoginScreen(viewModel, navController, onNavigateToRegister = { isLogin = false })
    } else {
        RegisterScreen(viewModel, onNavigateToLogin = { isLogin = true })
    }
}

@Composable
fun LoginScreen(viewModel: RiderViewModel, navController: NavController, onNavigateToRegister: () -> Unit) {"""
new_auth_flow = """@Composable
fun AuthFlow(viewModel: RiderViewModel, navController: NavHostController) {
    var currentScreen by remember { mutableStateOf("login") }
    
    when (currentScreen) {
        "login" -> LoginScreen(viewModel, navController, onNavigateToRegister = { currentScreen = "register" }, onNavigateToForgotPassword = { currentScreen = "forgot_password" })
        "register" -> RegisterScreen(viewModel, onNavigateToLogin = { currentScreen = "login" })
        "forgot_password" -> RiderForgotPasswordScreen(
            onNavigateToLogin = { currentScreen = "login" },
            onNavigateToDashboard = { navController.navigate("dashboard") { popUpTo(0) } }
        )
    }
}

@Composable
fun LoginScreen(viewModel: RiderViewModel, navController: NavController, onNavigateToRegister: () -> Unit, onNavigateToForgotPassword: () -> Unit = {}) {"""
content = content.replace(old_auth_flow, new_auth_flow)


# 5. Add Forgot Password button to Login Screen
old_login_bottom = """                    Button(
                        onClick = { viewModel.login(phone, password, context, onSuccess = { navController.navigate("dashboard") { popUpTo(0) } }) },
                        modifier = Modifier.fillMaxWidth().height(50.dp),
                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF03045E)),
                        enabled = !isLoading && phone.isNotBlank() && password.isNotBlank()
                    ) {
                        if (isLoading) CircularProgressIndicator(color = Color.White, modifier = Modifier.size(24.dp))
                        else Text("LOGIN", color = Color.White, fontWeight = FontWeight.Bold)
                    }
                }
            }
            
            Spacer(Modifier.height(24.dp))
            TextButton(onClick = onNavigateToRegister) {
                Text("New Rider? Apply Here", color = Color(0xFF00B4D8), fontWeight = FontWeight.Bold)
            }"""
new_login_bottom = """                    Button(
                        onClick = { viewModel.login(phone, password, context, onSuccess = { navController.navigate("dashboard") { popUpTo(0) } }) },
                        modifier = Modifier.fillMaxWidth().height(50.dp),
                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF03045E)),
                        enabled = !isLoading && phone.isNotBlank() && password.isNotBlank()
                    ) {
                        if (isLoading) CircularProgressIndicator(color = Color.White, modifier = Modifier.size(24.dp))
                        else Text("LOGIN", color = Color.White, fontWeight = FontWeight.Bold)
                    }
                }
            }
            
            Spacer(Modifier.height(16.dp))
            TextButton(onClick = onNavigateToForgotPassword) {
                Text("Forgot Password?", color = Color.White, fontWeight = FontWeight.Bold)
            }
            TextButton(onClick = onNavigateToRegister) {
                Text("New Rider? Apply Here", color = Color(0xFF00B4D8), fontWeight = FontWeight.Bold)
            }"""
content = content.replace(old_login_bottom, new_login_bottom)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
