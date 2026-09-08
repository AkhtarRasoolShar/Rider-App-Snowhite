with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Add _riderEmail state
old_zone = """    private val _riderZone = MutableStateFlow("")
    val riderZone: StateFlow<String> = _riderZone"""
new_zone = """    private val _riderZone = MutableStateFlow("")
    val riderZone: StateFlow<String> = _riderZone
    
    private val _riderEmail = MutableStateFlow("")
    val riderEmail: StateFlow<String> = _riderEmail"""
content = content.replace(old_zone, new_zone)

# Add riderEmail to initSession
old_init = """    fun initSession(context: Context) {
        val prefs = context.getSharedPreferences("RiderPrefs", Context.MODE_PRIVATE)
        _riderId.value = prefs.getInt("rider_id", -1)
        _riderName.value = prefs.getString("rider_name", "") ?: ""
        _riderPhone.value = prefs.getString("rider_phone", "") ?: ""
        _whatsappNumber.value = prefs.getString("whatsapp_number", "") ?: ""
        _riderZone.value = prefs.getString("rider_zones", "") ?: ""
        _homeAddress.value = prefs.getString("rider_address", "") ?: "" """
new_init = """    fun initSession(context: Context) {
        val prefs = context.getSharedPreferences("RiderPrefs", Context.MODE_PRIVATE)
        _riderId.value = prefs.getInt("rider_id", -1)
        _riderName.value = prefs.getString("rider_name", "") ?: ""
        _riderPhone.value = prefs.getString("rider_phone", "") ?: ""
        _riderEmail.value = prefs.getString("rider_email", "") ?: ""
        _whatsappNumber.value = prefs.getString("whatsapp_number", "") ?: ""
        _riderZone.value = prefs.getString("rider_zones", "") ?: ""
        _homeAddress.value = prefs.getString("rider_address", "") ?: "" """
content = content.replace(old_init, new_init)

# Add OTP Logic
otp_logic = """
    var showProfileOtpDialog by androidx.compose.runtime.mutableStateOf(false)
    var pendingProfileEmail by androidx.compose.runtime.mutableStateOf("")
    var pendingProfileWhatsapp by androidx.compose.runtime.mutableStateOf("")
    var isProfileUpdating by androidx.compose.runtime.mutableStateOf(false)

    fun requestProfileOtp(context: Context, newEmail: String, newWhatsapp: String) {
        if (newEmail.isBlank() || newWhatsapp.isBlank()) {
            Toast.makeText(context, "Email and WhatsApp cannot be empty", Toast.LENGTH_SHORT).show()
            return
        }
        pendingProfileEmail = newEmail
        pendingProfileWhatsapp = newWhatsapp
        isProfileUpdating = true
        
        viewModelScope.launch {
            try {
                val res = RetrofitClient.apiService.requestProfileUpdateOtp(ProfileUpdateOtpRequest(_riderId.value, newEmail))
                if (res.isSuccessful && res.body()?.status == "success") {
                    showProfileOtpDialog = true
                    Toast.makeText(context, res.body()?.message ?: "OTP sent to new email", Toast.LENGTH_SHORT).show()
                } else {
                    Toast.makeText(context, res.body()?.message ?: "Failed to send OTP", Toast.LENGTH_SHORT).show()
                }
            } catch (e: Exception) {
                Toast.makeText(context, "Error: ${e.message}", Toast.LENGTH_SHORT).show()
            } finally {
                isProfileUpdating = false
            }
        }
    }

    fun verifyProfileOtp(context: Context, otp: String, address: String, bankName: String, bankIban: String) {
        if (otp.isBlank()) {
            Toast.makeText(context, "Please enter OTP", Toast.LENGTH_SHORT).show()
            return
        }
        isProfileUpdating = true
        viewModelScope.launch {
            try {
                val res = RetrofitClient.apiService.verifyAndUpdateProfile(VerifyProfileUpdateRequest(
                    user_id = _riderId.value,
                    otp = otp,
                    new_phone = pendingProfileWhatsapp,
                    new_email = pendingProfileEmail
                ))
                if (res.isSuccessful && res.body()?.status == "success") {
                    res.body()?.data?.let {
                        SessionManager.saveUser(context, it)
                        _riderEmail.value = it.email ?: ""
                        _whatsappNumber.value = it.whatsapp_number ?: ""
                        _riderPhone.value = it.phone ?: ""
                        
                        saveProfileDetails(context, address, bankName, bankIban, _quickReply1.value, _quickReply2.value)
                        
                        showProfileOtpDialog = false
                        Toast.makeText(context, "Profile updated successfully!", Toast.LENGTH_SHORT).show()
                    } ?: run {
                        Toast.makeText(context, "Invalid response from server", Toast.LENGTH_SHORT).show()
                    }
                } else {
                    Toast.makeText(context, res.body()?.message ?: "Invalid OTP", Toast.LENGTH_SHORT).show()
                }
            } catch (e: Exception) {
                Toast.makeText(context, "Error: ${e.message}", Toast.LENGTH_SHORT).show()
            } finally {
                isProfileUpdating = false
            }
        }
    }
"""

content = content.replace("class RiderViewModel : ViewModel() {", "class RiderViewModel : ViewModel() {" + otp_logic)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
