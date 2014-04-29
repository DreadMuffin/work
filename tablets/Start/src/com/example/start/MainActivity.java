package com.example.start;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.Menu;
import android.view.View;
import android.widget.Button;

public class MainActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        
        final Button buttonA = (Button) findViewById(R.id.button_a);
        buttonA.setOnClickListener(new View.OnClickListener() {
        	@Override
			public void onClick(View v) {
				Intent LaunchIntent = getPackageManager().getLaunchIntentForPackage("com.example.agechoice_apps");
				startActivity(LaunchIntent);
			}
		});
        
        final Button buttonE = (Button) findViewById(R.id.button_e);
        buttonE.setOnClickListener(new View.OnClickListener() {
        	@Override
			public void onClick(View v) {
				Intent LaunchIntent = getPackageManager().getLaunchIntentForPackage("com.example.historie");
				startActivity(LaunchIntent);
			}
		});
        
        final Button buttonF = (Button) findViewById(R.id.button_f);
        buttonF.setOnClickListener(new View.OnClickListener() {
        	@Override
			public void onClick(View v) {
				Intent LaunchIntent = getPackageManager().getLaunchIntentForPackage("com.example.agechoice_movies");
				startActivity(LaunchIntent);
			}
		});
    }
    
    


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main, menu);
        return true;
    }
    
}
