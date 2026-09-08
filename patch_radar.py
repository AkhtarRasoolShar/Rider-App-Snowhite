import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Polling Logic Update
old_launched_effect = """    LaunchedEffect(Unit) {
        viewModel.fetchAvailableOrders(context)
    }"""
new_launched_effect = """    LaunchedEffect(Unit) {
        while (true) {
            viewModel.fetchAvailableOrders(context)
            kotlinx.coroutines.delay(10000)
        }
    }"""
content = content.replace(old_launched_effect, new_launched_effect)

# Radar Card UI Update
old_card = """                        Card(
                            elevation = CardDefaults.cardElevation(defaultElevation = 2.dp),
                            colors = CardDefaults.cardColors(containerColor = Color.White),
                            shape = RoundedCornerShape(16.dp),
                            modifier = Modifier.fillMaxWidth().clickable { selectedOrderForReview = order }
                        ) {
                            Column(modifier = Modifier.padding(16.dp).fillMaxWidth()) {
                                Row(
                                    modifier = Modifier.fillMaxWidth(),
                                    horizontalArrangement = Arrangement.SpaceBetween,
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Text(
                                        "Order #${order.orderId}",
                                        fontWeight = FontWeight.Black,
                                        color = Color(0xFF0F172A),
                                        fontSize = 16.sp
                                    )
                                    Text(
                                        "PKR ${order.totalAmount ?: "0"}",
                                        color = Color(0xFF00B4D8),
                                        fontWeight = FontWeight.Black,
                                        fontSize = 16.sp
                                    )
                                }
                                Spacer(Modifier.height(8.dp))
                                
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    Icon(Icons.Default.AccessTime, contentDescription = "Date", tint = Color(0xFF64748B), modifier = Modifier.size(14.dp))
                                    Spacer(Modifier.width(6.dp))
                                    Text(order.date ?: "Just now", color = Color(0xFF64748B), fontSize = 13.sp, maxLines = 1, overflow = TextOverflow.Ellipsis)
                                }
                                
                                Spacer(Modifier.height(12.dp))
                                HorizontalDivider(color = Color(0xFFF1F5F9))
                                Spacer(Modifier.height(12.dp))
                                
                                Row(
                                    modifier = Modifier.fillMaxWidth(),
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Icon(Icons.Default.Place, contentDescription = "Location", tint = Color(0xFF64748B), modifier = Modifier.size(20.dp))
                                    Spacer(Modifier.width(12.dp))
                                    Text(
                                        text = order.pickupAddress ?: "N/A", 
                                        fontSize = 14.sp, 
                                        modifier = Modifier.weight(1f),
                                        color = Color(0xFF334155),
                                        maxLines = 2,
                                        overflow = TextOverflow.Ellipsis
                                    )
                                    
                                    IconButton(
                                        onClick = {
                                            try {
                                                val gmmIntentUri = android.net.Uri.parse("geo:0,0?q=${android.net.Uri.encode(order.pickupAddress ?: "")}")
                                                val mapIntent = android.content.Intent(android.content.Intent.ACTION_VIEW, gmmIntentUri)
                                                mapIntent.setPackage("com.google.android.apps.maps")
                                                context.startActivity(mapIntent)
                                            } catch (e: Exception) {
                                                android.widget.Toast.makeText(context, "Google Maps is not installed", android.widget.Toast.LENGTH_SHORT).show()
                                            }
                                        },
                                        modifier = Modifier
                                            .size(40.dp)
                                            .background(Color(0xFFE0F2FE), shape = CircleShape)
                                    ) {
                                        Icon(
                                            imageVector = Icons.Default.Directions,
                                            contentDescription = "Navigate",
                                            tint = Color(0xFF0284C7),
                                            modifier = Modifier.size(20.dp)
                                        )
                                    }
                                }
                                
                                Spacer(Modifier.height(16.dp))
                                Button(
                                    onClick = { selectedOrderForReview = order },
                                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF00B4D8)),
                                    shape = RoundedCornerShape(12.dp),
                                    modifier = Modifier.fillMaxWidth().height(48.dp)
                                ) {
                                    Text("REVIEW & ACCEPT", fontSize = 14.sp, fontWeight = FontWeight.Bold, color = Color.White)
                                }
                            }
                        }"""
new_card = """                        Card(
                            elevation = CardDefaults.cardElevation(defaultElevation = 2.dp),
                            colors = CardDefaults.cardColors(containerColor = Color.White),
                            shape = RoundedCornerShape(16.dp),
                            border = androidx.compose.foundation.BorderStroke(1.dp, Color(0xFFF1F5F9)),
                            modifier = Modifier.fillMaxWidth().clickable { selectedOrderForReview = order }
                        ) {
                            Column(modifier = Modifier.padding(16.dp).fillMaxWidth()) {
                                Row(
                                    modifier = Modifier.fillMaxWidth(),
                                    horizontalArrangement = Arrangement.SpaceBetween,
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Text(
                                        "Order #${order.orderId}",
                                        fontWeight = FontWeight.ExtraBold,
                                        color = Color(0xFF0F172A),
                                        fontSize = 17.sp
                                    )
                                    Text(
                                        "PKR ${order.totalAmount ?: "0"}",
                                        color = TealAccent,
                                        fontWeight = FontWeight.ExtraBold,
                                        fontSize = 18.sp
                                    )
                                }
                                Spacer(Modifier.height(6.dp))
                                
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    Icon(Icons.Default.AccessTime, contentDescription = "Date", tint = Color(0xFF94A3B8), modifier = Modifier.size(14.dp))
                                    Spacer(Modifier.width(6.dp))
                                    Text(order.date ?: "Just now", color = Color(0xFF64748B), fontSize = 13.sp, maxLines = 1, overflow = TextOverflow.Ellipsis)
                                }
                                
                                Spacer(Modifier.height(16.dp))
                                
                                Row(
                                    modifier = Modifier.fillMaxWidth(),
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Icon(Icons.Default.LocationOn, contentDescription = "Location", tint = TealAccent, modifier = Modifier.size(24.dp))
                                    Spacer(Modifier.width(12.dp))
                                    Text(
                                        text = order.pickupAddress ?: "N/A", 
                                        fontSize = 15.sp, 
                                        modifier = Modifier.weight(1f),
                                        color = Color(0xFF334155),
                                        fontWeight = FontWeight.SemiBold,
                                        maxLines = 2,
                                        overflow = TextOverflow.Ellipsis
                                    )
                                    
                                    IconButton(
                                        onClick = {
                                            try {
                                                val gmmIntentUri = android.net.Uri.parse("geo:0,0?q=${android.net.Uri.encode(order.pickupAddress ?: "")}")
                                                val mapIntent = android.content.Intent(android.content.Intent.ACTION_VIEW, gmmIntentUri)
                                                mapIntent.setPackage("com.google.android.apps.maps")
                                                context.startActivity(mapIntent)
                                            } catch (e: Exception) {
                                                android.widget.Toast.makeText(context, "Google Maps is not installed", android.widget.Toast.LENGTH_SHORT).show()
                                            }
                                        },
                                        modifier = Modifier
                                            .size(40.dp)
                                            .background(Color(0xFFF1F5F9), shape = CircleShape)
                                    ) {
                                        Icon(
                                            imageVector = Icons.Default.Directions,
                                            contentDescription = "Navigate",
                                            tint = TealAccent,
                                            modifier = Modifier.size(20.dp)
                                        )
                                    }
                                }
                                
                                Spacer(Modifier.height(20.dp))
                                Button(
                                    onClick = { selectedOrderForReview = order },
                                    colors = ButtonDefaults.buttonColors(containerColor = TealAccent),
                                    shape = RoundedCornerShape(12.dp),
                                    modifier = Modifier.fillMaxWidth().height(52.dp)
                                ) {
                                    Text("REVIEW & ACCEPT", fontSize = 14.sp, fontWeight = FontWeight.ExtraBold, color = Color.White)
                                }
                            }
                        }"""
content = content.replace(old_card, new_card)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
