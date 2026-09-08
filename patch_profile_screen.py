import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

start_str = "fun ProfileScreen(viewModel: RiderViewModel, navController: NavHostController) {"
end_str = "@OptIn(ExperimentalMaterial3Api::class)\n@Composable\nfun QuickRepliesScreen"

start_idx = content.find(start_str)
end_idx = content.find(end_str)

# Backtrack start_idx to include the @Composable annotation if it exists
composable_idx = content.rfind("@Composable", 0, start_idx)
if composable_idx != -1 and start_idx - composable_idx < 30:
    start_idx = composable_idx

new_profile = """@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ProfileScreen(viewModel: RiderViewModel, navController: NavHostController) {
    val context = LocalContext.current
    val name by viewModel.riderName.collectAsState()
    val zone by viewModel.riderZone.collectAsState()
    val riderEmail by viewModel.riderEmail.collectAsState()
    
    var emailInput by remember { mutableStateOf(riderEmail) }
    var address by remember { mutableStateOf(viewModel.homeAddress.value) }
    var bankName by remember { mutableStateOf(viewModel.bankName.value) }
    var bankIban by remember { mutableStateOf(viewModel.bankIban.value) }
    var whatsapp by remember { mutableStateOf(if (viewModel.whatsappNumber.value.isNotEmpty()) viewModel.whatsappNumber.value else viewModel.riderPhone.value) }

    val scrollState = rememberScrollState()

    // OTP State
    var otpInput by remember { mutableStateOf("") }

    if (viewModel.showProfileOtpDialog) {
        androidx.compose.material3.AlertDialog(
            onDismissRequest = { viewModel.showProfileOtpDialog = false },
            title = { Text("Verify Email", fontWeight = FontWeight.Bold) },
            text = {
                Column {
                    Text("Enter the OTP sent to your registered email.")
                    Spacer(Modifier.height(16.dp))
                    OutlinedTextField(
                        value = otpInput,
                        onValueChange = { otpInput = it },
                        label = { Text("OTP Code") },
                        modifier = Modifier.fillMaxWidth(),
                        singleLine = true,
                        keyboardOptions = androidx.compose.foundation.text.KeyboardOptions(keyboardType = androidx.compose.ui.text.input.KeyboardType.Number)
                    )
                }
            },
            confirmButton = {
                Button(
                    onClick = { viewModel.verifyProfileOtp(context, otpInput, address, bankName, bankIban) },
                    enabled = !viewModel.isProfileUpdating
                ) {
                    if (viewModel.isProfileUpdating) CircularProgressIndicator(color = Color.White, modifier = Modifier.size(16.dp))
                    else Text("Verify & Save")
                }
            },
            dismissButton = {
                TextButton(onClick = { viewModel.showProfileOtpDialog = false }) {
                    Text("Cancel", color = ErrorRed)
                }
            }
        )
    }

    Box(modifier = Modifier.fillMaxSize().background(Color(0xFFF8F9FA))) {
        // Gradient Header Background
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .height(240.dp)
                .background(
                    brush = androidx.compose.ui.graphics.Brush.verticalGradient(
                        colors = listOf(TealAccent, DarkBlue)
                    ),
                    shape = RoundedCornerShape(bottomStart = 32.dp, bottomEnd = 32.dp)
                )
        )
        
        Column(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(scrollState),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Spacer(modifier = Modifier.height(100.dp))
            
            // Profile Info Overlapping Card
            Card(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 24.dp),
                shape = RoundedCornerShape(24.dp),
                colors = CardDefaults.cardColors(containerColor = Color.White),
                elevation = CardDefaults.cardElevation(defaultElevation = 8.dp)
            ) {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(24.dp),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Box(
                        modifier = Modifier
                            .size(90.dp)
                            .background(Color(0xFFE0F2FE), CircleShape),
                        contentAlignment = Alignment.Center
                    ) {
                        Text(
                            if (name.isNotEmpty()) name.take(1).uppercase() else "U",
                            fontSize = 36.sp,
                            fontWeight = FontWeight.Bold,
                            color = TealAccent
                        )
                    }
                    Spacer(Modifier.height(16.dp))
                    Text(name.ifEmpty { "Driver Name" }, fontWeight = FontWeight.ExtraBold, fontSize = 24.sp, color = Color(0xFF1E293B))
                    Spacer(Modifier.height(8.dp))
                    Surface(color = Color(0xFFF1F5F9), shape = RoundedCornerShape(16.dp)) {
                        Text(
                            "Hubs: ${zone.ifEmpty { "Unassigned" }}",
                            modifier = Modifier.padding(horizontal = 16.dp, vertical = 6.dp),
                            color = Color(0xFF475569),
                            fontWeight = FontWeight.SemiBold,
                            fontSize = 13.sp
                        )
                    }
                    
                    Spacer(Modifier.height(24.dp))
                    // Stats Row
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceEvenly
                    ) {
                        StatItem(icon = Icons.Default.DirectionsCar, label = "Orders Today", value = "12")
                        StatItem(icon = Icons.Default.Star, label = "Rating", value = "4.8★")
                    }
                }
            }
            
            Spacer(modifier = Modifier.height(24.dp))
            
            // Editable Fields Section
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 24.dp)
            ) {
                Text("Account Details", color = Color(0xFF64748B), fontWeight = FontWeight.Bold, fontSize = 14.sp)
                Spacer(Modifier.height(12.dp))
                
                OutlinedTextField(
                    value = emailInput,
                    onValueChange = { emailInput = it },
                    label = { Text("Email Address") },
                    leadingIcon = { Icon(Icons.Default.Email, contentDescription = null, tint = TealAccent) },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedBorderColor = TealAccent,
                        unfocusedBorderColor = Color(0xFFE2E8F0)
                    )
                )
                Spacer(Modifier.height(12.dp))
                
                OutlinedTextField(
                    value = address,
                    onValueChange = { address = it },
                    label = { Text("Home Address") },
                    leadingIcon = { Icon(Icons.Default.Home, contentDescription = null, tint = TealAccent) },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedBorderColor = TealAccent,
                        unfocusedBorderColor = Color(0xFFE2E8F0)
                    )
                )
                Spacer(Modifier.height(12.dp))
                OutlinedTextField(
                    value = whatsapp,
                    onValueChange = { whatsapp = it },
                    label = { Text("WhatsApp Number") },
                    leadingIcon = { Icon(Icons.Default.Phone, contentDescription = null, tint = TealAccent) },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedBorderColor = TealAccent,
                        unfocusedBorderColor = Color(0xFFE2E8F0)
                    )
                )
                
                Spacer(Modifier.height(24.dp))
                Text("Bank Information", color = Color(0xFF64748B), fontWeight = FontWeight.Bold, fontSize = 14.sp)
                Spacer(Modifier.height(12.dp))
                
                OutlinedTextField(
                    value = bankName,
                    onValueChange = { bankName = it },
                    label = { Text("Bank Name") },
                    leadingIcon = { Icon(Icons.Default.AccountBalance, contentDescription = null, tint = TealAccent) },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedBorderColor = TealAccent,
                        unfocusedBorderColor = Color(0xFFE2E8F0)
                    )
                )
                Spacer(Modifier.height(12.dp))
                OutlinedTextField(
                    value = bankIban,
                    onValueChange = { bankIban = it },
                    label = { Text("IBAN / Account Number") },
                    leadingIcon = { Icon(Icons.Default.AccountBalanceWallet, contentDescription = null, tint = TealAccent) },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedBorderColor = TealAccent,
                        unfocusedBorderColor = Color(0xFFE2E8F0)
                    )
                )
                
                Spacer(Modifier.height(32.dp))
                Button(
                    onClick = { 
                        if (emailInput != riderEmail || whatsapp != viewModel.whatsappNumber.value) {
                            viewModel.requestProfileOtp(context, emailInput, whatsapp)
                        } else {
                            viewModel.saveProfileDetails(context, address, bankName, bankIban, viewModel.quickReply1.value, viewModel.quickReply2.value)
                            viewModel.updateWhatsApp(context, whatsapp)
                            Toast.makeText(context, "Profile updated successfully!", Toast.LENGTH_SHORT).show()
                        }
                    },
                    modifier = Modifier.fillMaxWidth().height(56.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = TealAccent),
                    shape = RoundedCornerShape(16.dp),
                    enabled = !viewModel.isProfileUpdating
                ) {
                    if (viewModel.isProfileUpdating && !viewModel.showProfileOtpDialog) CircularProgressIndicator(color = Color.White, modifier = Modifier.size(24.dp))
                    else Text("SAVE CHANGES", color = Color.White, fontWeight = FontWeight.ExtraBold, fontSize = 16.sp)
                }
                
                Spacer(Modifier.height(32.dp))
                Text("Preferences & Settings", color = Color(0xFF64748B), fontWeight = FontWeight.Bold, fontSize = 14.sp)
                Spacer(Modifier.height(12.dp))
                
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(16.dp),
                    colors = CardDefaults.cardColors(containerColor = Color.White),
                    elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
                ) {
                    Column {
                        SettingsRow(icon = Icons.Default.Chat, text = "Manage Quick Replies", onClick = { navController.navigate("quickReplies") })
                        HorizontalDivider(color = Color(0xFFF1F5F9))
                        SettingsRow(icon = Icons.Default.SupportAgent, text = "Contact Support", onClick = {
                            val intent = Intent(Intent.ACTION_VIEW, Uri.parse("https://wa.me/923001234567"))
                            try { context.startActivity(intent) } catch (e: Exception) { Toast.makeText(context, "WhatsApp not installed", Toast.LENGTH_SHORT).show() }
                        })
                        HorizontalDivider(color = Color(0xFFF1F5F9))
                        SettingsRow(icon = Icons.Default.Logout, text = "Logout", isDestructive = true, onClick = {
                            viewModel.logout(context)
                            navController.navigate("auth") { popUpTo(0) }
                        })
                    }
                }
                Spacer(Modifier.height(40.dp))
            }
        }
    }
}
"""

new_content = content[:start_idx] + new_profile + "\n" + content[end_idx:]

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(new_content)
