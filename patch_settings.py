with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Make get_app_settings fail silently without a log crash/spam, since backend throws error
old_fetch_settings = """    fun fetchSettings() {
        viewModelScope.launch {
            try {
                val response = RetrofitClient.apiService.getAppSettings()
                if (response.isSuccessful) {
                    response.body()?.data?.let {
                        appSettings = it
                    }
                } else {
                    android.util.Log.e("AppSettings", "Server Error: ${response.code()}")
                }
            } catch (e: Exception) {
                e.printStackTrace()
                android.util.Log.e("AppSettings", "Network Error: ${e.message}")
            }
        }
    }"""
new_fetch_settings = """    fun fetchSettings() {
        viewModelScope.launch {
            try {
                val response = RetrofitClient.apiService.getAppSettings()
                if (response.isSuccessful && response.body()?.status == "success") {
                    response.body()?.data?.let {
                        appSettings = it
                    }
                } else {
                    // Backend returned error for app settings, ignore silently as fallback values are used.
                    android.util.Log.w("AppSettings", "Failed to fetch settings, using defaults.")
                }
            } catch (e: Exception) {
                android.util.Log.w("AppSettings", "Network error fetching settings, using defaults.")
            }
        }
    }"""
content = content.replace(old_fetch_settings, new_fetch_settings)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
