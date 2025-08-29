#!/bin/bash

# Узнаем архитектуру
ARCH=$(uname -m)
echo "Архитектура: $ARCH"

# Создаем правильный AndroidManifest.xml
cat > AndroidManifest.xml << 'EOF'
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.lightmessenger"
    android:versionCode="1"
    android:versionName="1.0">

    <uses-sdk android:minSdkVersion="16" android:targetSdkVersion="28"/>
    
    <application
        android:allowBackup="true"
        android:label="Light Messenger"
        android:theme="@android:style/Theme.Light">
        
        <activity android:name=".MainActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

        <activity android:name=".ChatActivity" />
    </application>
</manifest>
EOF

echo "✅ Создан манифест для старых устройств"
echo "Минимальная версия: Android 4.1 (Jelly Bean)"
