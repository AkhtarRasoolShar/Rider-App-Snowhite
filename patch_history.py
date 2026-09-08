import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# 1. Update StatusBadge
old_badge = """fun StatusBadge(status: String) {
    val formattedStatus = status.replace("_", " ")
        .lowercase()
        .split(" ")
        .joinToString(" ") { it.replaceFirstChar { char -> char.uppercase() } }
    
    val (bgColor, textColor) = when (status.uppercase()) {
        "DELIVERED" -> Color(0xFFE8F5E9) to Color(0xFF2E7D32)
        "OUT_FOR_DELIVERY" -> Color(0xFFE3F2FD) to Color(0xFF1565C0)
        "IN_WASHING", "RECEIVED_AT_HUB" -> Color(0xFFFFF3E0) to Color(0xFFEF6C00)
        "COLLECTING", "PENDING" -> Color(0xFFEDE7F6) to Color(0xFF4527A0)
        else -> Color(0xFFF5F5F5) to Color(0xFF616161)
    }

    Box(
        modifier = Modifier
            .background(bgColor, RoundedCornerShape(8.dp))
            .padding(horizontal = 12.dp, vertical = 6.dp)
    ) {
        Text(
            text = formattedStatus,
            color = textColor,
            fontSize = 12.sp,
            fontWeight = FontWeight.Bold
        )
    }
}"""
new_badge = """fun StatusBadge(status: String) {
    val formattedStatus = status.replace("_", " ")
        .lowercase()
        .split(" ")
        .joinToString(" ") { it.replaceFirstChar { char -> char.uppercase() } }
    
    val (bgColor, textColor) = when (status.uppercase()) {
        "DELIVERED" -> Color(0xFFDCFCE7) to Color(0xFF166534)
        "OUT_FOR_DELIVERY" -> Color(0xFFDBEAFE) to Color(0xFF1E40AF)
        "IN_WASHING" -> Color(0xFFE0E7FF) to Color(0xFF3730A3)
        "RECEIVED_AT_HUB" -> Color(0xFFFFEDD5) to Color(0xFFC2410C)
        "COLLECTING", "PENDING" -> Color(0xFFFEF9C3) to Color(0xFF854D0E)
        else -> Color(0xFFF1F5F9) to Color(0xFF475569)
    }

    Box(
        modifier = Modifier
            .background(bgColor, RoundedCornerShape(50))
            .padding(horizontal = 14.dp, vertical = 6.dp)
    ) {
        Text(
            text = formattedStatus,
            color = textColor,
            fontSize = 12.sp,
            fontWeight = FontWeight.ExtraBold
        )
    }
}"""
content = content.replace(old_badge, new_badge)


# 2. Update LazyColumn Items
old_card = """                        androidx.compose.material3.ElevatedCard(
                            elevation = CardDefaults.elevatedCardElevation(defaultElevation = 4.dp), 
                            colors = CardDefaults.elevatedCardColors(containerColor = Color.White), 
                            shape = RoundedCornerShape(16.dp),
                            modifier = Modifier.fillMaxWidth().clickable { selectedOrderForUpdate = order }
                        ) {
                            Column(modifier = Modifier.fillMaxWidth().padding(16.dp)) {
                                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.Top) {
                                    Column {
                                        Text("Order #${order.orderId}", fontWeight = FontWeight.Bold, color = Color(0xFF03045E), fontSize = 16.sp)
                                        Spacer(Modifier.height(4.dp))
                                        Text(order.date ?: "N/A", color = Color.Gray, fontSize = 12.sp)
                                    }
                                    Text("PKR ${order.totalAmount ?: "0"}", color = Color(0xFF00B4D8), fontWeight = FontWeight.ExtraBold, fontSize = 16.sp)
                                }
                                
                                Spacer(Modifier.height(12.dp))
                                StatusBadge(status = currentStatus)
                                Spacer(Modifier.height(16.dp))
                                
                                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalAlignment = Alignment.CenterVertically) {
                                        Button(
                                            onClick = { showStatusDialogForOrder = order },
                                            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF00B4D8)),
                                            shape = RoundedCornerShape(8.dp),
                                            contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp)
                                        ) {
                                            Text("Update Status", fontSize = 12.sp, color = Color.White, fontWeight = FontWeight.Bold)
                                        }
                                        androidx.compose.material3.OutlinedButton(
                                            onClick = { selectedOrderForUpdate = order },
                                            shape = RoundedCornerShape(8.dp),
                                            contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp)
                                        ) {
                                            Text("View Details", fontSize = 12.sp, color = Color(0xFF03045E))
                                        }
                                    }
                                    IconButton(
                                        onClick = { navController.navigate("chat/${order.orderId}") },
                                        modifier = Modifier.background(Color(0xFFE3F2FD), androidx.compose.foundation.shape.CircleShape).size(40.dp)
                                    ) {
                                        Icon(androidx.compose.material.icons.Icons.Default.Email, contentDescription = "Chat", tint = Color(0xFF1565C0), modifier = Modifier.size(20.dp))
                                    }
                                }
                            }
                        }"""
new_card = """                        androidx.compose.material3.Card(
                            colors = CardDefaults.cardColors(containerColor = Color.White),
                            shape = RoundedCornerShape(16.dp),
                            border = androidx.compose.foundation.BorderStroke(1.dp, Color(0xFFF1F5F9)),
                            modifier = Modifier.fillMaxWidth().clickable { selectedOrderForUpdate = order }
                        ) {
                            Column(modifier = Modifier.fillMaxWidth().padding(16.dp)) {
                                // TOP ROW
                                Row(
                                    modifier = Modifier.fillMaxWidth(),
                                    horizontalArrangement = Arrangement.SpaceBetween,
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Text(
                                        text = "Order #${order.orderId}",
                                        fontWeight = FontWeight.ExtraBold,
                                        color = Color(0xFF0F172A),
                                        fontSize = 17.sp
                                    )
                                    Text(
                                        text = "PKR ${order.totalAmount ?: "0"}",
                                        color = TealAccent,
                                        fontWeight = FontWeight.ExtraBold,
                                        fontSize = 16.sp
                                    )
                                }
                                
                                Spacer(Modifier.height(12.dp))
                                
                                // MIDDLE SECTION
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    Icon(Icons.Default.Schedule, contentDescription = null, tint = Color(0xFF94A3B8), modifier = Modifier.size(16.dp))
                                    Spacer(Modifier.width(6.dp))
                                    Text(order.date ?: "N/A", color = Color(0xFF64748B), fontSize = 13.sp, fontWeight = FontWeight.Medium)
                                }
                                
                                Spacer(Modifier.height(8.dp))
                                
                                val displayCustomer = order.customerName?.takeIf { it.isNotBlank() } ?: "Unknown Customer"
                                val displayAddress = order.pickupAddress?.takeIf { it.isNotBlank() } ?: "No Address Provided"
                                
                                Row(verticalAlignment = Alignment.Top) {
                                    Icon(Icons.Default.Person, contentDescription = null, tint = Color(0xFF94A3B8), modifier = Modifier.size(16.dp))
                                    Spacer(Modifier.width(6.dp))
                                    Column {
                                        Text(displayCustomer, color = Color(0xFF334155), fontSize = 14.sp, fontWeight = FontWeight.Bold)
                                        Text(displayAddress, color = Color(0xFF64748B), fontSize = 13.sp, maxLines = 1, overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis)
                                    }
                                }
                                
                                Spacer(Modifier.height(16.dp))
                                StatusBadge(status = currentStatus)
                                
                                Spacer(Modifier.height(16.dp))
                                HorizontalDivider(color = Color(0xFFF1F5F9))
                                Spacer(Modifier.height(16.dp))
                                
                                // BOTTOM ACTION BAR
                                Row(
                                    modifier = Modifier.fillMaxWidth(),
                                    horizontalArrangement = Arrangement.SpaceBetween,
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalAlignment = Alignment.CenterVertically) {
                                        androidx.compose.material3.OutlinedButton(
                                            onClick = { selectedOrderForUpdate = order },
                                            shape = RoundedCornerShape(12.dp),
                                            contentPadding = PaddingValues(horizontal = 14.dp, vertical = 8.dp),
                                            border = androidx.compose.foundation.BorderStroke(1.dp, Color(0xFFE2E8F0))
                                        ) {
                                            Text("View Details", fontSize = 12.sp, color = Color(0xFF334155), fontWeight = FontWeight.SemiBold)
                                        }
                                        Button(
                                            onClick = { showStatusDialogForOrder = order },
                                            colors = ButtonDefaults.buttonColors(containerColor = TealAccent),
                                            shape = RoundedCornerShape(12.dp),
                                            contentPadding = PaddingValues(horizontal = 14.dp, vertical = 8.dp)
                                        ) {
                                            Text("Update Status", fontSize = 12.sp, color = Color.White, fontWeight = FontWeight.Bold)
                                        }
                                    }
                                    IconButton(
                                        onClick = { navController.navigate("chat/${order.orderId}") },
                                        modifier = Modifier.background(Color(0xFFF1F5F9), CircleShape).size(40.dp)
                                    ) {
                                        Icon(Icons.AutoMirrored.Filled.Chat, contentDescription = "Chat", tint = TealAccent, modifier = Modifier.size(18.dp))
                                    }
                                }
                            }
                        }"""
content = content.replace(old_card, new_card)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
