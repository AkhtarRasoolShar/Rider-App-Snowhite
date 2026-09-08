with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# 1. Login Screen
old_login = """                if (!viewModel.appSettings.logo_url.isNullOrEmpty()) {
                    coil.compose.AsyncImage(
                        model = viewModel.appSettings.logo_url,
                        contentDescription = "App Logo",
                        modifier = Modifier.size(60.dp)
                    )
                } else {
                    Icon(Icons.Default.LocalShipping, contentDescription = null, modifier = Modifier.size(60.dp), tint = Color.White)
                }"""
new_login = """                val logo = viewModel.appSettings.logo_url
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

# 2. Register Screen
old_register = """                    val logo = viewModel.appSettings.logo_url
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
new_register = """                    val logo = viewModel.appSettings.logo_url
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

# 3. Splash Screen
old_splash = """        if (!logo.isNullOrEmpty()) {
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
        }"""
new_splash = """        if (!logo.isNullOrEmpty()) {
            coil.compose.AsyncImage(
                model = logo,
                contentDescription = "App Logo",
                modifier = Modifier.size(120.dp),
                contentScale = ContentScale.Fit
            )
        } else {
            Icon(Icons.Default.LocalShipping, contentDescription = null, modifier = Modifier.size(120.dp), tint = Color(0xFF1565C0))
        }"""

content = content.replace(old_login, new_login)
content = content.replace(old_register, new_register)
content = content.replace(old_splash, new_splash)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
