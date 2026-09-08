import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Update RiderLoginRequest
content = re.sub(
    r'data class RiderLoginRequest\(@SerializedName\("email"\) val email: String\? = null, val password: String, val is_rider_app: Boolean = true\)',
    'data class RiderLoginRequest(@SerializedName("email") val email: String? = null, @SerializedName("phone") val phone: String? = null, val password: String, val is_rider_app: Boolean = true)',
    content
)

# Update LoginScreen
content = content.replace(
    'var email by remember { mutableStateOf("") }',
    'var email by remember { mutableStateOf("") } // Actually emailOrPhone'
)
content = content.replace(
    'label = { Text("Email Address") },',
    'label = { Text("Email or Phone Number") },'
)
content = content.replace(
    'keyboardOptions = androidx.compose.foundation.text.KeyboardOptions(keyboardType = androidx.compose.ui.text.input.KeyboardType.Email),',
    'keyboardOptions = androidx.compose.foundation.text.KeyboardOptions(keyboardType = androidx.compose.ui.text.input.KeyboardType.Text),'
)

# Update ViewModel login function signature
content = content.replace(
    'fun login(email: String, pass: String, context: Context, onSuccess: () -> Unit) {',
    'fun login(emailOrPhone: String, pass: String, context: Context, onSuccess: () -> Unit) {'
)

# Update ViewModel login API call
old_api_call = 'val res = RetrofitClient.apiService.login(RiderLoginRequest(email, pass))'
new_api_call = '''val req = if (emailOrPhone.contains("@")) RiderLoginRequest(email = emailOrPhone, password = pass) else RiderLoginRequest(phone = emailOrPhone, password = pass)
                val res = RetrofitClient.apiService.login(req)'''
content = content.replace(old_api_call, new_api_call)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
