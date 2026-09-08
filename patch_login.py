import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# 1. RiderLoginRequest
content = content.replace(
    'data class RiderLoginRequest(@SerializedName("phone") val phone: String? = null, val password: String, val is_rider_app: Boolean = true)',
    'data class RiderLoginRequest(@SerializedName("email") val email: String? = null, val password: String, val is_rider_app: Boolean = true)'
)

# 2. fun login in ViewModel
content = content.replace(
    'fun login(phone: String, pass: String, context: Context, onSuccess: () -> Unit) {',
    'fun login(email: String, pass: String, context: Context, onSuccess: () -> Unit) {'
)
content = content.replace(
    'val res = RetrofitClient.apiService.login(RiderLoginRequest(phone, pass))',
    'val res = RetrofitClient.apiService.login(RiderLoginRequest(email, pass))'
)

# 3. fun register in ViewModel
content = content.replace(
    'fun register(name: String, phone: String, pass: String, zones: List<String>, email: String, context: Context) {',
    'fun register(name: String, phone: String, pass: String, zones: List<String>, email: String, context: Context, onSuccess: () -> Unit) {'
)
old_register_success = """                if (response.isSuccessful) {
                    val body = response.body()
                    if (body?.status == "success" && body.data != null) {
                        _pendingApproval.value = true
                        _authError.value = "Registration Successful. Awaiting Admin Approval."
                    } else {
                        _authError.value = body?.message ?: "Registration Failed."
                    }"""
new_register_success = """                if (response.isSuccessful) {
                    val body = response.body()
                    if (body?.status == "success") {
                        onSuccess()
                    } else {
                        _authError.value = body?.message ?: "Registration Failed."
                    }"""
content = content.replace(old_register_success, new_register_success)


with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
