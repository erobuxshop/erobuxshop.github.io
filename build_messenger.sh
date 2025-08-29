#!/bin/bash

echo "🐣 Создаем проект Light Messenger..."

# Создаем структуру папок
mkdir -p LightMessenger/app/src/main/java/com/example/lightmessenger/
mkdir -p LightMessenger/app/src/main/res/layout/
mkdir -p LightMessenger/app/src/main/res/drawable/

echo "📁 Структура папок создана"

# Создаем AndroidManifest.xml
cat > LightMessenger/app/src/main/AndroidManifest.xml << 'EOF'
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.lightmessenger">

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

# Создаем layout files
cat > LightMessenger/app/src/main/res/layout/activity_main.xml << 'EOF'
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="20dp"
    android:gravity="center">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Light Messenger"
        android:textSize="24sp"
        android:textStyle="bold"
        android:layout_marginBottom="30dp"/>

    <EditText
        android:id="@+id/etUsername"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:hint="Ваше имя"
        android:layout_marginBottom="20dp"
        android:padding="15dp"/>

    <Button
        android:id="@+id/btnLogin"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Войти в чат"/>
</LinearLayout>
EOF

cat > LightMessenger/app/src/main/res/layout/activity_chat.xml << 'EOF'
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical">

    <ListView
        android:id="@+id/lvMessages"
        android:layout_width="match_parent"
        android:layout_height="0dp"
        android:layout_weight="1"/>

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal"
        android:padding="10dp">

        <EditText
            android:id="@+id/etMessage"
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_weight="1"
            android:hint="Сообщение"
            android:padding="10dp"/>

        <Button
            android:id="@+id/btnSend"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="➤"
            android:padding="15dp"/>
    </LinearLayout>
</LinearLayout>
EOF

# Создаем Java классы
cat > LightMessenger/app/src/main/java/com/example/lightmessenger/MainActivity.java << 'EOF'
package com.example.lightmessenger;

import android.content.Intent;
import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;
import android.app.Activity;

public class MainActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        EditText etUsername = (EditText) findViewById(R.id.etUsername);
        Button btnLogin = (Button) findViewById(R.id.btnLogin);
        
        btnLogin.setOnClickListener(v -> {
            String username = etUsername.getText().toString().trim();
            if (username.isEmpty()) {
                Toast.makeText(MainActivity.this, "Введите имя", Toast.LENGTH_SHORT).show();
            } else {
                Intent intent = new Intent(MainActivity.this, ChatActivity.class);
                intent.putExtra("USERNAME", username);
                startActivity(intent);
                finish();
            }
        });
    }
}
EOF

cat > LightMessenger/app/src/main/java/com/example/lightmessenger/ChatActivity.java << 'EOF'
package com.example.lightmessenger;

import android.os.Bundle;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import java.util.ArrayList;
import android.app.Activity;

public class ChatActivity extends Activity {
    private ArrayList<String> messages = new ArrayList<>();
    private ArrayAdapter<String> adapter;
    private String username;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_chat);

        username = getIntent().getStringExtra("USERNAME");
        ListView lvMessages = (ListView) findViewById(R.id.lvMessages);
        EditText etMessage = (EditText) findViewById(R.id.etMessage);
        Button btnSend = (Button) findViewById(R.id.btnSend);

        messages.add("Добро пожаловать, " + username + "!");
        adapter = new ArrayAdapter<>(this, android.R.layout.simple_list_item_1, messages);
        lvMessages.setAdapter(adapter);

        btnSend.setOnClickListener(v -> {
            String message = etMessage.getText().toString().trim();
            if (!message.isEmpty()) {
                messages.add(username + ": " + message);
                adapter.notifyDataSetChanged();
                etMessage.setText("");
                lvMessages.smoothScrollToPosition(messages.size() - 1);
            }
        });
    }
}
EOF

echo "✅ Все файлы созданы!"
echo "📁 Проект находится в: ~/LightMessenger/"
echo "🎯 Теперь откри папку в AIDE или файловом менеджере"
