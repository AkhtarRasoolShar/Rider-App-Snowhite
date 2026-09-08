with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

old_fetch = """    fun fetchSettings() {
        viewModelScope.launch {
            try {
                val response = RetrofitClient.apiService.getAppSettings()
                if (response.isSuccessful) {
                    response.body()?.data?.let {
                        appSettings = it
                    }
                }
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }"""
new_fetch = """    fun fetchSettings() {
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

content = content.replace(old_fetch, new_fetch)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
