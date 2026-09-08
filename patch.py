with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# 1. Update AppSettings
old_appsettings = """data class AppSettings(
    val app_name: String? = null,
    val logo_url: String? = null
)"""
new_appsettings = """data class AppSettings(
    val app_name: String? = null,
    val logo_url: String? = null,
    val launcher_icon_url: String? = null
)"""
content = content.replace(old_appsettings, new_appsettings)

# 2. Add API method
old_api = """    @GET("routes.php?action=get_hubs")
    suspend fun getHubs(): Response<GenericResponse<List<Hub>>>"""
new_api = """    @GET("routes.php?action=get_app_settings")
    suspend fun getAppSettings(): Response<GenericResponse<AppSettings>>

    @GET("routes.php?action=get_hubs")
    suspend fun getHubs(): Response<GenericResponse<List<Hub>>>"""
content = content.replace(old_api, new_api)

# 3. Add fetchSettings in ViewModel
old_init = """    init {
        fetchHubs()
    }"""
new_init = """    init {
        fetchSettings()
        fetchHubs()
    }
    
    fun fetchSettings() {
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
content = content.replace(old_init, new_init)

# 4. Create SplashScreen composable
splash_screen = """
@Composable
fun SplashScreen(viewModel: RiderViewModel) {
    val logo = viewModel.appSettings.launcher_icon_url ?: viewModel.appSettings.logo_url
    Box(
        modifier = Modifier.fillMaxSize().background(Color.White),
        contentAlignment = Alignment.Center
    ) {
        if (!logo.isNullOrEmpty()) {
            coil.compose.AsyncImage(
                model = logo,
                contentDescription = "App Logo",
                modifier = Modifier.size(120.dp),
                fallback = androidx.compose.ui.res.painterResource(R.drawable.snowhite_logo),
                error = androidx.compose.ui.res.painterResource(R.drawable.snowhite_logo)
            )
        } else {
            androidx.compose.foundation.Image(
                painter = androidx.compose.ui.res.painterResource(R.drawable.snowhite_logo),
                contentDescription = "App Logo",
                modifier = Modifier.size(120.dp)
            )
        }
    }
}
"""
content = content.replace("// --- Screens ---", "// --- Screens ---\n" + splash_screen)

# 5. Update setContent navigation
old_nav = """                androidx.compose.runtime.LaunchedEffect(riderId) {
                    if (riderId != -1) {
                        navController.navigate("dashboard") { popUpTo(0) }
                    } else {
                        navController.navigate("auth") { popUpTo(0) }
                    }
                }
                
                androidx.navigation.compose.NavHost(navController = navController, startDestination = "auth") {"""
new_nav = """                androidx.navigation.compose.NavHost(navController = navController, startDestination = "splash") {
                    composable("splash") {
                        SplashScreen(viewModel)
                        androidx.compose.runtime.LaunchedEffect(Unit) {
                            kotlinx.coroutines.delay(2000)
                            if (riderId != -1) {
                                navController.navigate("dashboard") { popUpTo(0) }
                            } else {
                                navController.navigate("auth") { popUpTo(0) }
                            }
                        }
                    }"""
content = content.replace(old_nav, new_nav)

# 6. Update Login/Register screen logo
old_logo = """                    if (!viewModel.appSettings.logo_url.isNullOrEmpty()) {
                        coil.compose.AsyncImage(
                            model = viewModel.appSettings.logo_url,
                            contentDescription = "App Logo",
                            modifier = Modifier.size(60.dp)
                        )
                    } else {
                        Icon(Icons.Default.LocalShipping, contentDescription = null, modifier = Modifier.size(60.dp), tint = Color.White)
                    }"""
new_logo = """                    val logo = viewModel.appSettings.logo_url
                    if (!logo.isNullOrEmpty()) {
                        coil.compose.AsyncImage(
                            model = logo,
                            contentDescription = "App Logo",
                            modifier = Modifier.size(80.dp),
                            fallback = androidx.compose.ui.res.painterResource(R.drawable.snowhite_logo),
                            error = androidx.compose.ui.res.painterResource(R.drawable.snowhite_logo)
                        )
                    } else {
                        androidx.compose.foundation.Image(
                            painter = androidx.compose.ui.res.painterResource(R.drawable.snowhite_logo),
                            contentDescription = "App Logo",
                            modifier = Modifier.size(80.dp)
                        )
                    }"""
content = content.replace(old_logo, new_logo)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
