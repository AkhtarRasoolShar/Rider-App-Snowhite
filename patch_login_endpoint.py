with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

content = content.replace(
    '@POST("routes.php?action=login")\n    suspend fun login(',
    '@POST("routes.php?action=rider_login")\n    suspend fun login('
)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
