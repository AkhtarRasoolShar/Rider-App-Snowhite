with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

old_models = """data class RiderOrder(
    @SerializedName("order_id") val orderId: String? = null,
    @SerializedName("pickup_address") val pickupAddress: String? = null,
    @SerializedName("total_amount") val totalAmount: String? = null,
    @SerializedName("date") val date: String? = null,
    @SerializedName("status") val status: String? = null,
    @SerializedName("items") val items: List<OrderItem>? = emptyList(),
    @SerializedName("zone") val zone: String? = null,
    @SerializedName("customer_name") val customerName: String? = null,
    @SerializedName("customer_phone") val customerPhone: String? = null,
    var distanceInMeters: Float? = null
)

data class OrderItem(
    @SerializedName("name") val name: String? = null,
    @SerializedName("quantity") val quantity: String? = null
)"""
new_models = """data class RiderOrder(
    @SerializedName("order_id") val orderId: String? = null,
    @SerializedName("pickup_address") val pickupAddress: String? = null,
    @SerializedName("total_amount") val totalAmount: String? = null,
    @SerializedName("date") val date: String? = null,
    @SerializedName("status") val status: String? = null,
    @SerializedName("items") val items: List<OrderItem>? = emptyList(),
    @SerializedName("zone") val zone: String? = null,
    @SerializedName("customer_name") val customerName: String? = null,
    @SerializedName("customer_phone") val customerPhone: String? = null,
    @SerializedName("special_notes") val specialNotes: String? = null,
    var distanceInMeters: Float? = null
)

data class OrderItem(
    @SerializedName("item") val name: String? = null,
    @SerializedName("qty") val quantity: Int? = null,
    @SerializedName("price") val price: Double? = null,
    @SerializedName("product_image") val productImage: String? = null
)"""
content = content.replace(old_models, new_models)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
