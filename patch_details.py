import re

with open("app/src/main/java/com/example/RiderUI.kt", "r") as f:
    content = f.read()

start_str = "fun OrderDetailsSheetContent("
end_str = "    }\n}"

start_idx = content.find(start_str)
end_idx = content.find(end_str, start_idx) + len(end_str)

if start_idx == -1 or end_idx == -1:
    print("Bounds not found")
    exit(1)
    
new_sheet = """fun OrderDetailsSheetContent(
    order: RiderOrder,
    isHistory: Boolean,
    onAccept: (() -> Unit)? = null,
    onReject: (() -> Unit)? = null,
    onUpdateStatus: ((String) -> Unit)? = null,
    onPrint: (() -> Unit)? = null,
    onChat: (() -> Unit)? = null
) {
    val context = androidx.compose.ui.platform.LocalContext.current
    Column(modifier = Modifier.fillMaxWidth().padding(24.dp).padding(bottom = 32.dp)) {
        // --- HEADER ---
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
            Column {
                Text(if (isHistory) "Active Order Details" else "Review Order", fontSize = 20.sp, fontWeight = FontWeight.Bold, color = Color(0xFF0F172A))
                Spacer(Modifier.height(8.dp))
                Surface(color = Color(0xFFE0F2FE), shape = RoundedCornerShape(8.dp)) {
                    Text("Order #${order.orderId ?: 0}", modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp), color = Color(0xFF0369A1), fontWeight = FontWeight.Bold)
                }
            }
            if (isHistory && onPrint != null) {
                IconButton(onClick = onPrint, modifier = Modifier.background(Color(0xFFF1F5F9), androidx.compose.foundation.shape.CircleShape)) {
                    Icon(androidx.compose.material.icons.Icons.Default.Print, contentDescription = "Print Receipt", tint = Color(0xFF00B4D8))
                }
            }
        }
        Spacer(Modifier.height(24.dp))
        
        // --- SPECIAL NOTES (WARNING) ---
        if (!order.specialNotes.isNullOrBlank()) {
            Card(
                colors = CardDefaults.cardColors(containerColor = Color(0xFFFEF9C3)),
                elevation = CardDefaults.cardElevation(0.dp),
                shape = RoundedCornerShape(12.dp),
                modifier = Modifier.fillMaxWidth().padding(bottom = 16.dp)
            ) {
                Row(modifier = Modifier.padding(16.dp), verticalAlignment = Alignment.Top) {
                    Icon(Icons.Default.Info, contentDescription = "Info", tint = Color(0xFFCA8A04))
                    Spacer(Modifier.width(8.dp))
                    Column {
                        Text("Special Instructions", fontWeight = FontWeight.Bold, color = Color(0xFF854D0E), fontSize = 14.sp)
                        Spacer(Modifier.height(4.dp))
                        Text(order.specialNotes, color = Color(0xFFA16207), fontSize = 14.sp)
                    }
                }
            }
        }

        // --- CUSTOMER & PICKUP INFO ---
        Card(
            colors = CardDefaults.cardColors(containerColor = Color.White),
            border = androidx.compose.foundation.BorderStroke(1.dp, Color(0xFFF1F5F9)),
            elevation = CardDefaults.cardElevation(0.dp),
            shape = RoundedCornerShape(12.dp),
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                // Customer Name & Call
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(Icons.Default.Person, contentDescription = "Customer", tint = Color(0xFF94A3B8), modifier = Modifier.size(20.dp))
                        Spacer(Modifier.width(12.dp))
                        Column {
                            Text(order.customerName ?: "Unknown Customer", fontWeight = FontWeight.Bold, fontSize = 16.sp, color = Color(0xFF0F172A))
                            Text(order.customerPhone ?: "No Phone", color = Color(0xFF64748B), fontSize = 14.sp)
                        }
                    }
                    if (!order.customerPhone.isNullOrEmpty()) {
                        IconButton(
                            onClick = {
                                val intent = Intent(Intent.ACTION_DIAL, Uri.parse("tel:${order.customerPhone}"))
                                context.startActivity(intent)
                            },
                            modifier = Modifier.background(Color(0xFFDCFCE7), androidx.compose.foundation.shape.CircleShape)
                        ) {
                            Icon(Icons.Default.Phone, contentDescription = "Call", tint = Color(0xFF166534))
                        }
                    }
                }
                
                Spacer(Modifier.height(16.dp))
                HorizontalDivider(color = Color(0xFFF1F5F9))
                Spacer(Modifier.height(16.dp))
                
                // Pickup Address & Navigate
                Row(modifier = Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
                    Icon(Icons.Default.LocationOn, contentDescription = "Location", tint = Color(0xFF94A3B8), modifier = Modifier.size(20.dp))
                    Spacer(Modifier.width(12.dp))
                    Text(
                        text = order.pickupAddress ?: "Unknown Location", 
                        fontSize = 14.sp, 
                        modifier = Modifier.weight(1f),
                        color = Color(0xFF334155),
                        lineHeight = 20.sp
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
                            .background(Color(0xFFE0F2FE), shape = androidx.compose.foundation.shape.CircleShape)
                    ) {
                        Icon(
                            imageVector = Icons.Default.Directions,
                            contentDescription = "Navigate",
                            tint = Color(0xFF0284C7),
                            modifier = Modifier.size(20.dp)
                        )
                    }
                }
            }
        }
        Spacer(Modifier.height(24.dp))
        
        // --- DETAILED GARMENT BREAKDOWN ---
        val orderItems = order.items
        if (!orderItems.isNullOrEmpty()) {
            Text("Garments Breakdown", fontSize = 16.sp, fontWeight = FontWeight.ExtraBold, color = Color(0xFF0F172A))
            Spacer(Modifier.height(12.dp))
            LazyColumn(
                modifier = Modifier.fillMaxWidth().heightIn(max = 240.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                items(orderItems) { item ->
                    Card(
                        colors = CardDefaults.cardColors(containerColor = Color.White),
                        border = androidx.compose.foundation.BorderStroke(1.dp, Color(0xFFF1F5F9)),
                        shape = RoundedCornerShape(12.dp)
                    ) {
                        Row(
                            modifier = Modifier.fillMaxWidth().padding(12.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            // Mocking Image since the API doesn't provide item images right now
                            AsyncImage(
                                model = "https://images.pexels.com/photos/4505458/pexels-photo-4505458.jpeg?auto=compress&cs=tinysrgb&w=150",
                                contentDescription = item.name,
                                contentScale = ContentScale.Crop,
                                modifier = Modifier
                                    .size(50.dp)
                                    .clip(RoundedCornerShape(8.dp))
                                    .background(Color(0xFFF8F9FA))
                            )
                            Spacer(Modifier.width(12.dp))
                            Column(modifier = Modifier.weight(1f)) {
                                Text(item.name ?: "Garment Item", color = Color(0xFF0F172A), fontWeight = FontWeight.Bold, fontSize = 15.sp)
                                Spacer(Modifier.height(4.dp))
                                Text("Qty: ${item.quantity ?: 1}", color = Color(0xFF64748B), fontSize = 13.sp)
                            }
                            Text(
                                text = "PKR ${item.price?.toInt() ?: 0}",
                                fontWeight = FontWeight.ExtraBold,
                                color = Color(0xFF00B4D8),
                                fontSize = 14.sp
                            )
                        }
                    }
                }
            }
            Spacer(Modifier.height(24.dp))
        } else {
            Text("No item details found.", color = Color.Gray)
            Spacer(Modifier.height(24.dp))
        }
        
        HorizontalDivider(color = Color(0xFFF1F5F9))
        Spacer(Modifier.height(24.dp))
        
        // --- MASSIVE TOTAL AMOUNT ---
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
            Text("Total Amount", fontSize = 16.sp, color = Color(0xFF64748B), fontWeight = FontWeight.Medium)
            Text("PKR ${order.totalAmount ?: "0"}", color = Color(0xFF00B4D8), fontWeight = FontWeight.Black, fontSize = 26.sp)
        }
        Spacer(Modifier.height(24.dp))
        
        // --- ACTIONS ---
        if (isHistory && onUpdateStatus != null) {
            // Reusing existing status map logic but applying new button styles
            val statusMap = listOf("Pending" to "Collected", "Collected" to "In Process", "In Process" to "Out for Delivery", "Out for Delivery" to "Delivered")
            val currentStatus = order.status ?: "Pending"
            val nextStatus = statusMap.find { it.first == currentStatus }?.second
            
            if (nextStatus != null) {
                Button(
                    onClick = { onUpdateStatus(nextStatus) },
                    modifier = Modifier.fillMaxWidth().height(56.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF00B4D8)),
                    shape = RoundedCornerShape(12.dp)
                ) {
                    Text("Mark as $nextStatus", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color.White)
                }
                Spacer(Modifier.height(12.dp))
            }
            if (onChat != null) {
                OutlinedButton(
                    onClick = onChat,
                    modifier = Modifier.fillMaxWidth().height(56.dp),
                    shape = RoundedCornerShape(12.dp),
                    border = androidx.compose.foundation.BorderStroke(1.dp, Color(0xFFE2E8F0))
                ) {
                    Icon(Icons.AutoMirrored.Filled.Chat, contentDescription = "Chat", tint = Color(0xFF334155), modifier = Modifier.padding(end = 8.dp))
                    Text("Chat with Customer", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color(0xFF334155))
                }
            }
        } else if (!isHistory && onAccept != null && onReject != null) {
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                OutlinedButton(
                    onClick = onReject,
                    modifier = Modifier.weight(1f).height(56.dp),
                    colors = ButtonDefaults.outlinedButtonColors(contentColor = Color(0xFFEF4444)), // Red 500
                    shape = RoundedCornerShape(12.dp),
                    border = androidx.compose.foundation.BorderStroke(2.dp, Color(0xFFFCA5A5))
                ) {
                    Text("Reject", fontSize = 16.sp, fontWeight = FontWeight.Bold)
                }
                Button(
                    onClick = onAccept,
                    modifier = Modifier.weight(1f).height(56.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF00B4D8)),
                    shape = RoundedCornerShape(12.dp)
                ) {
                    Text("Accept Order", fontSize = 16.sp, fontWeight = FontWeight.ExtraBold, color = Color.White)
                }
            }
        }
    }
}"""

content = content[:start_idx] + new_sheet + content[end_idx:]

with open("app/src/main/java/com/example/RiderUI.kt", "w") as f:
    f.write(content)
