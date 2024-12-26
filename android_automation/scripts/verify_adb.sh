#!/bin/bash

check_adb_connection() {
    echo "=== ADB Connection Verification ===" && echo
    # Check ADB server status
    echo "1. Verifying ADB server..."
    adb version >/dev/null 2>&1 || { echo "Error: ADB not running"; exit 1; }

    # Check for devices
    echo "2. Checking for connected devices..."
    devices=$(adb devices | grep -v "List" | grep "device$")
    if [ -n "$devices" ]; then
        echo "Found connected devices:"
        echo "$devices"

        # Test basic ADB commands
        echo "3. Testing ADB connection..."
        for device in $(echo "$devices" | cut -f1); do
            echo "Testing device: $device"
            adb -s "$device" shell getprop ro.product.model
        done
        echo "Connection verification successful"
        exit 0
    else
        echo "No devices connected. Please:"
        echo "1. Enable Developer Options"
        echo "2. Enable USB Debugging"
        echo "3. Enable Wireless Debugging"
        echo "4. Run: adb connect <device-ip>:port"
        exit 1
    fi
}

check_adb_connection
