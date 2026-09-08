import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# 1. Remove fetchSettings call from initSession
init_session_old = """    fun initSession(context: android.content.Context) {
        val prefs = context.getSharedPreferences("RiderPrefs", android.content.Context.MODE_PRIVATE)
        _riderId.value = prefs.getInt("rider_id", -1)
        _riderName.value = prefs.getString("rider_name", "") ?: ""
        _riderPhone.value = prefs.getString("rider_phone", "") ?: ""
        _whatsappNumber.value = prefs.getString("whatsapp_number", "") ?: ""
        _riderZone.value = prefs.getString("rider_zones", "") ?: ""

        fetchSettings()
        fetchHubs()
        
        loadProfileDetails(context)
        startPolling(context)
    }"""

init_session_new = """    fun initSession(context: android.content.Context) {
        val prefs = context.getSharedPreferences("RiderPrefs", android.content.Context.MODE_PRIVATE)
        _riderId.value = prefs.getInt("rider_id", -1)
        _riderName.value = prefs.getString("rider_name", "") ?: ""
        _riderPhone.value = prefs.getString("rider_phone", "") ?: ""
        _whatsappNumber.value = prefs.getString("whatsapp_number", "") ?: ""
        _riderZone.value = prefs.getString("rider_zones", "") ?: ""

        fetchHubs()
        
        loadProfileDetails(context)
        startPolling(context)
    }"""
content = content.replace(init_session_old, init_session_new)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
