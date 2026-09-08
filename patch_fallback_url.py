with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# 1. Login Screen
old_login = """                val logo = viewModel.appSettings.logo_url
                if (!logo.isNullOrEmpty()) {
                    coil.compose.AsyncImage(
                        model = logo,
                        contentDescription = "App Logo",
                        modifier = Modifier.size(80.dp),
                        contentScale = ContentScale.Fit
                    )
                } else {
                    Icon(Icons.Default.LocalShipping, contentDescription = null, modifier = Modifier.size(80.dp), tint = Color.White)
                }"""
new_login = """                val customFallbackUrl = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRSDAJkXtsNkzYsDhu_BhNUwLD82d47UMkHFx2JCjoZFw&s"
                val targetLogoUrl = viewModel.appSettings.logo_url?.takeIf { it.isNotBlank() } ?: customFallbackUrl

                coil.compose.AsyncImage(
                    model = coil.request.ImageRequest.Builder(LocalContext.current)
                        .data(targetLogoUrl)
                        .crossfade(true)
                        .build(),
                    contentDescription = "App Logo",
                    modifier = Modifier.size(80.dp),
                    contentScale = ContentScale.Fit
                )"""

# 2. Register Screen
old_register = """                    val logo = viewModel.appSettings.logo_url
                    if (!logo.isNullOrEmpty()) {
                        coil.compose.AsyncImage(
                            model = logo,
                            contentDescription = "App Logo",
                            modifier = Modifier.size(80.dp),
                            contentScale = ContentScale.Fit
                        )
                    } else {
                        Icon(Icons.Default.LocalShipping, contentDescription = null, modifier = Modifier.size(80.dp), tint = Color.White)
                    }"""
new_register = """                    val customFallbackUrl = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRSDAJkXtsNkzYsDhu_BhNUwLD82d47UMkHFx2JCjoZFw&s"
                    val targetLogoUrl = viewModel.appSettings.logo_url?.takeIf { it.isNotBlank() } ?: customFallbackUrl

                    coil.compose.AsyncImage(
                        model = coil.request.ImageRequest.Builder(LocalContext.current)
                            .data(targetLogoUrl)
                            .crossfade(true)
                            .build(),
                        contentDescription = "App Logo",
                        modifier = Modifier.size(80.dp),
                        contentScale = ContentScale.Fit
                    )"""

# 3. Splash Screen
old_splash = """    val logo = viewModel.appSettings.launcher_icon_url ?: viewModel.appSettings.logo_url
    Box(
        modifier = Modifier.fillMaxSize().background(Color.White),
        contentAlignment = Alignment.Center
    ) {
        if (!logo.isNullOrEmpty()) {
            coil.compose.AsyncImage(
                model = logo,
                contentDescription = "App Logo",
                modifier = Modifier.size(120.dp),
                contentScale = ContentScale.Fit
            )
        } else {
            Icon(Icons.Default.LocalShipping, contentDescription = null, modifier = Modifier.size(120.dp), tint = Color(0xFF1565C0))
        }
    }"""
new_splash = """    val customFallbackUrl = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRSDAJkXtsNkzYsDhu_BhNUwLD82d47UMkHFx2JCjoZFw&s"
    val backendLogo = viewModel.appSettings.launcher_icon_url?.takeIf { it.isNotBlank() } 
        ?: viewModel.appSettings.logo_url?.takeIf { it.isNotBlank() }
    val targetLogoUrl = backendLogo ?: customFallbackUrl

    Box(
        modifier = Modifier.fillMaxSize().background(Color.White),
        contentAlignment = Alignment.Center
    ) {
        coil.compose.AsyncImage(
            model = coil.request.ImageRequest.Builder(LocalContext.current)
                .data(targetLogoUrl)
                .crossfade(true)
                .build(),
            contentDescription = "App Logo",
            modifier = Modifier.size(120.dp),
            contentScale = ContentScale.Fit
        )
    }"""

content = content.replace(old_login, new_login)
content = content.replace(old_register, new_register)
content = content.replace(old_splash, new_splash)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
