import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

start_str = "fun RiderDashboardScreen(viewModel: RiderViewModel, onNavigateToRadar: () -> Unit) {"
end_str = "@Composable\nfun MainAppScreen(viewModel: RiderViewModel) {"

start_idx = content.find(start_str)
end_idx = content.find(end_str)

if start_idx == -1 or end_idx == -1:
    print("Could not find bounds")
    exit(1)
    
composable_idx = content.rfind("@Composable", 0, start_idx)
if composable_idx != -1 and start_idx - composable_idx < 30:
    start_idx = composable_idx

new_dash = """@Composable
fun RiderDashboardScreen(viewModel: RiderViewModel, onNavigateToRadar: () -> Unit) {
    val context = LocalContext.current
    val riderName by viewModel.riderName.collectAsState()
    val myOrders by viewModel.myOrders.collectAsState()
    
    LaunchedEffect(Unit) {
        viewModel.fetchMyOrders(context)
    }
    
    val completedOrders = myOrders.count { it.status == "DELIVERED" }
    val totalEarnings = myOrders.filter { it.status == "DELIVERED" }.sumOf { it.totalAmount?.toDoubleOrNull() ?: 0.0 }
    
    // Take the 5 most recent orders for the dashboard
    val recentOrders = myOrders.take(5)

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFFF8F9FA)) 
            .verticalScroll(rememberScrollState())
            .padding(20.dp)
    ) {
        // --- HEADER SECTION ---
        Row(
            verticalAlignment = Alignment.CenterVertically,
            modifier = Modifier.fillMaxWidth().padding(bottom = 24.dp, top = 8.dp)
        ) {
            Column {
                Text("Welcome back,", color = Color(0xFF64748B), fontSize = 14.sp)
                Text(text = riderName.ifEmpty { "Captain" }, fontSize = 24.sp, fontWeight = FontWeight.ExtraBold, color = Color(0xFF0F172A))
            }
        }

        // --- STATS CARDS SECTION ---
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
            // Earnings Card
            Card(
                modifier = Modifier.weight(1f).height(120.dp),
                shape = RoundedCornerShape(16.dp),
                colors = CardDefaults.cardColors(containerColor = TealAccent),
                elevation = CardDefaults.cardElevation(defaultElevation = 4.dp)
            ) {
                Column(modifier = Modifier.padding(16.dp).fillMaxSize(), verticalArrangement = Arrangement.SpaceBetween) {
                    Icon(Icons.Default.AccountBalanceWallet, contentDescription = null, tint = Color.White)
                    Column {
                        Text("Total Earnings", color = Color.White.copy(alpha = 0.8f), fontSize = 12.sp, fontWeight = FontWeight.Medium)
                        Text("PKR $totalEarnings", color = Color.White, fontSize = 20.sp, fontWeight = FontWeight.ExtraBold)
                    }
                }
            }

            // Completed Orders Card
            Card(
                modifier = Modifier.weight(1f).height(120.dp),
                shape = RoundedCornerShape(16.dp),
                colors = CardDefaults.cardColors(containerColor = Color.White),
                border = androidx.compose.foundation.BorderStroke(1.dp, Color(0xFFF1F5F9)),
                elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
            ) {
                Column(modifier = Modifier.padding(16.dp).fillMaxSize(), verticalArrangement = Arrangement.SpaceBetween) {
                    Icon(Icons.Default.CheckCircle, contentDescription = null, tint = Color(0xFF10B981))
                    Column {
                        Text("Completed Orders", color = Color(0xFF64748B), fontSize = 12.sp, fontWeight = FontWeight.Medium)
                        Text("$completedOrders", color = Color(0xFF0F172A), fontSize = 20.sp, fontWeight = FontWeight.ExtraBold)
                    }
                }
            }
        }

        Spacer(modifier = Modifier.height(24.dp))

        // --- QUICK ACTION (RADAR) ---
        Text("Quick Actions", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color(0xFF0F172A), modifier = Modifier.padding(bottom = 12.dp))
        Button(
            onClick = { onNavigateToRadar() },
            modifier = Modifier.fillMaxWidth().height(56.dp),
            colors = ButtonDefaults.buttonColors(containerColor = DarkBlue),
            shape = RoundedCornerShape(12.dp)
        ) {
            Icon(Icons.Default.Radar, contentDescription = null, tint = Color.White)
            Spacer(modifier = Modifier.width(12.dp))
            Text("Go to Radar (Find Orders)", color = Color.White, fontSize = 16.sp, fontWeight = FontWeight.Bold)
        }

        Spacer(modifier = Modifier.height(32.dp))

        // --- RECENT ORDERS (HISTORY) SECTION ---
        Row(
            modifier = Modifier.fillMaxWidth().padding(bottom = 12.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text("Recent Orders", fontSize = 18.sp, fontWeight = FontWeight.Bold, color = Color(0xFF0F172A))
        }

        if (recentOrders.isEmpty()) {
            Box(modifier = Modifier.fillMaxWidth().padding(top = 32.dp), contentAlignment = Alignment.Center) {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Icon(Icons.AutoMirrored.Filled.ListAlt, contentDescription = null, modifier = Modifier.size(48.dp), tint = Color(0xFFCBD5E1))
                    Spacer(modifier = Modifier.height(8.dp))
                    Text("No recent orders found.", color = Color(0xFF64748B), fontSize = 14.sp)
                }
            }
        } else {
            recentOrders.forEach { order ->
                Card(
                    modifier = Modifier.fillMaxWidth().padding(bottom = 12.dp),
                    colors = CardDefaults.cardColors(containerColor = Color.White),
                    border = androidx.compose.foundation.BorderStroke(1.dp, Color(0xFFF1F5F9)),
                    shape = RoundedCornerShape(16.dp)
                ) {
                    Row(
                        modifier = Modifier.padding(16.dp).fillMaxWidth(),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        Column(modifier = Modifier.weight(1f)) {
                            Text("Order #${order.orderId}", fontWeight = FontWeight.ExtraBold, fontSize = 16.sp, color = Color(0xFF0F172A))
                            Spacer(modifier = Modifier.height(4.dp))
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Icon(Icons.Default.AccessTime, contentDescription = null, tint = Color(0xFF94A3B8), modifier = Modifier.size(12.dp))
                                Spacer(Modifier.width(4.dp))
                                Text(order.date ?: "", fontSize = 12.sp, color = Color(0xFF64748B), fontWeight = FontWeight.Medium)
                            }
                        }
                        
                        Column(horizontalAlignment = Alignment.End) {
                            Text(
                                text = "PKR ${order.totalAmount}", 
                                fontWeight = FontWeight.ExtraBold, 
                                fontSize = 16.sp, 
                                color = TealAccent
                            )
                            Spacer(modifier = Modifier.height(8.dp))
                            StatusBadge(status = order.status ?: "PENDING")
                        }
                    }
                }
            }
        }
    }
}

"""

new_content = content[:start_idx] + new_dash + content[end_idx:]

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(new_content)
