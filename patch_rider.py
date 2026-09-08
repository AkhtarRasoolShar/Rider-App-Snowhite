import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# 1. Add Requests
requests = """data class ResetPasswordWithOtpRequest(val email: String, val otp: String, val new_password: String)
data class ProfileUpdateOtpRequest(val user_id: Int, val new_email: String)
data class VerifyProfileUpdateRequest(val user_id: Int, val otp: String, val new_phone: String, val new_email: String)"""
content = content.replace("data class ResetPasswordWithOtpRequest(val email: String, val otp: String, val new_password: String)", requests)

# 2. Add email to RiderAuthData
old_auth = """data class RiderAuthData(
    @SerializedName("id") val id: Int = -1,
    @SerializedName("name") val name: String? = null,
    @SerializedName("phone") val phone: String? = null,
    @SerializedName("service_zone") val service_zone: String? = null,
    @SerializedName("status") val status: String? = null,
    val whatsapp_number: String? = null
)"""
new_auth = """data class RiderAuthData(
    @SerializedName("id") val id: Int = -1,
    @SerializedName("name") val name: String? = null,
    @SerializedName("phone") val phone: String? = null,
    @SerializedName("email") val email: String? = null,
    @SerializedName("service_zone") val service_zone: String? = null,
    @SerializedName("status") val status: String? = null,
    val whatsapp_number: String? = null
)"""
content = content.replace(old_auth, new_auth)

# 3. Add to ApiService
api = """    @Headers("Content-Type: application/json")
    @POST("routes.php?action=reset_password_with_otp")
    suspend fun resetPassword(@Body request: ResetPasswordWithOtpRequest): Response<GenericResponse<RiderAuthData>>

    @Headers("Content-Type: application/json")
    @POST("routes.php?action=request_profile_update_otp")
    suspend fun requestProfileUpdateOtp(@Body request: ProfileUpdateOtpRequest): Response<GenericResponse<Any>>

    @Headers("Content-Type: application/json")
    @POST("routes.php?action=verify_and_update_profile")
    suspend fun verifyAndUpdateProfile(@Body request: VerifyProfileUpdateRequest): Response<GenericResponse<RiderAuthData>>"""
content = content.replace("""    @Headers("Content-Type: application/json")
    @POST("routes.php?action=reset_password_with_otp")
    suspend fun resetPassword(@Body request: ResetPasswordWithOtpRequest): Response<GenericResponse<RiderAuthData>>""", api)

# 4. Update SessionManager
old_save_user = """        prefs.edit().apply {
            putInt("rider_id", data.id)
            putString("rider_name", data.name)
            putString("rider_phone", data.phone)
            putString("whatsapp_number", data.whatsapp_number ?: "")
            putString("rider_zones", data.service_zone ?: "")
        }.apply()"""
new_save_user = """        prefs.edit().apply {
            putInt("rider_id", data.id)
            putString("rider_name", data.name)
            putString("rider_phone", data.phone)
            putString("rider_email", data.email ?: "")
            putString("whatsapp_number", data.whatsapp_number ?: "")
            putString("rider_zones", data.service_zone ?: "")
        }.apply()"""
content = content.replace(old_save_user, new_save_user)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
