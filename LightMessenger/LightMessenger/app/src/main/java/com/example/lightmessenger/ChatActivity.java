package com.example.lightmessenger;

import android.os.Bundle;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import java.util.ArrayList;
import androidx.appcompat.app.AppCompatActivity;

public class ChatActivity extends AppCompatActivity {
    private ArrayList<String> messages = new ArrayList<>();
    private ArrayAdapter<String> adapter;
    private String username;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_chat);

        username = getIntent().getStringExtra("USERNAME");
        ListView lvMessages = findViewById(R.id.lvMessages);
        EditText etMessage = findViewById(R.id.etMessage);
        Button btnSend = findViewById(R.id.btnSend);

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
