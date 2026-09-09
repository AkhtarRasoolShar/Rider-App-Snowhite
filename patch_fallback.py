with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    code = f.read()

fallback_block = """                // Fallback in case of HTTP 500 or Network Error
                availableHubs = listOf(
                    Hub(1, "Clifton"),
                    Hub(2, "Tariq Road"),
                    Hub(3, "DHA"),
                    Hub(4, "Gulshan")
                )"""

code = code.replace(fallback_block, "")

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(code)
