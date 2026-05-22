[app]

# Title of your application
title = SecureCall

# Package name
package.name = securecall

# Package domain (usually com.yourname)
package.domain = com.securecall

# Source code directory
source.dir = .

# Source files to include
source.include_exts = py,png,jpg,kv,atlas

# Version
version = 1.0

# Requirements
requirements = python3,kivy==2.3.0,opencv-python-headless,websockets,asyncio

# Application orientation
orientation = portrait

# Fullscreen
fullscreen = 1

# Android permissions
android.permissions = INTERNET, CAMERA, RECORD_AUDIO, MODIFY_AUDIO_SETTINGS, WAKE_LOCK

# Android API levels
android.api = 33
android.minapi = 24

# NDK version
android.ndk = 25b

# Architectures
android.archs = arm64-v8a, armeabi-v7a

# App icon (optional - later you can add)
# icon.filename = icon.png

[buildozer]

# Log level (higher = more details)
log_level = 2

# Warn if running as root
warn_on_root = 1

# Build directory
build_dir = .buildozer

# Bin directory
bin_dir = bin