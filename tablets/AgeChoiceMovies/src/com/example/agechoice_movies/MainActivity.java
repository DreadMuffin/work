package com.example.agechoice_movies;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.Menu;
import android.view.View;
import android.widget.Button;
import com.example.agechoice_movies.R;

public class MainActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        final Button buttonA = (Button) findViewById(R.id.button_nul);
        buttonA.setOnClickListener(new View.OnClickListener() {
        	@Override
			public void onClick(View v) {
				Intent LaunchIntent = getPackageManager().getLaunchIntentForPackage("com.example.agelist0");
				startActivity(LaunchIntent);
			}
		});

        final Button buttonB = (Button) findViewById(R.id.button_tre);
        buttonB.setOnClickListener(new View.OnClickListener() {
        	@Override
			public void onClick(View v) {
				Intent LaunchIntent = getPackageManager().getLaunchIntentForPackage("com.example.movielist7");
				startActivity(LaunchIntent);
			}
		});

        final Button buttonC = (Button) findViewById(R.id.button_syv);
        buttonC.setOnClickListener(new View.OnClickListener() {
        	@Override
			public void onClick(View v) {
				Intent LaunchIntent = getPackageManager().getLaunchIntentForPackage("com.example.movielist3");
				startActivity(LaunchIntent);
			}
		});

        final Button buttonD = (Button) findViewById(R.id.button_ti);
        buttonD.setOnClickListener(new View.OnClickListener() {
        	@Override
			public void onClick(View v) {
				Intent LaunchIntent = getPackageManager().getLaunchIntentForPackage("com.example.movielist10");
				startActivity(LaunchIntent);
			}
		});

        final Button buttonE = (Button) findViewById(R.id.button_tolv);
        buttonE.setOnClickListener(new View.OnClickListener() {
        	@Override
			public void onClick(View v) {
				Intent LaunchIntent = getPackageManager().getLaunchIntentForPackage("com.example.movielist12");
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