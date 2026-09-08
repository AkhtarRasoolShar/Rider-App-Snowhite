import re

def fix_worker():
    with open("app/src/main/java/com/example/OrderPollingWorker.kt", "r") as f:
        content = f.read()
    
    # Just grab everything after "class OrderPollingWorker"
    idx = content.find("class OrderPollingWorker")
    if idx == -1: return
    body = content[idx:]
    
    imports = """package com.example

import android.app.NotificationChannel
import android.app.NotificationManager
import android.content.Context
import android.content.pm.PackageManager
import android.os.Build
import androidx.core.app.ActivityCompat
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters
import retrofit2.Response

"""
    with open("app/src/main/java/com/example/OrderPollingWorker.kt", "w") as f:
        f.write(imports + body)

def fix_main():
    with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
        content = f.read()

    idx = content.find("// --- Colors ---")
    if idx == -1: return
    body = content[idx:]

    imports = """package com.example

import android.Manifest
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.location.Geocoder
import android.location.Location
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.util.Log
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.result.contract.ActivityResultContracts
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.compose.animation.*
import androidx.compose.foundation.*
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.*
import androidx.compose.foundation.lazy.grid.*
import androidx.compose.foundation.shape.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.*
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.core.app.ActivityCompat
import androidx.core.view.WindowCompat
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavController
import androidx.navigation.NavHostController
import androidx.navigation.compose.*
import androidx.work.*
import coil.compose.AsyncImage
import com.example.ui.theme.RiderTheme
import com.google.android.gms.location.LocationServices
import retrofit2.http.Headers
import java.util.concurrent.TimeUnit
import kotlin.reflect.KProperty

"""
    with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
        f.write(imports + body)

fix_worker()
fix_main()
