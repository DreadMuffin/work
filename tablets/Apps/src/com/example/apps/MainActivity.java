package com.example.apps;


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
        
        final Button button1 = (Button) findViewById(R.id.button_galaxy);
        button1.setOnClickListener(new View.OnClickListener() {
        	@Override
			public void onClick(View v) {
				Intent LaunchIntent = getPackageManager().getLaunchIntentForPackage("com.maxelus.shadowgalaxylivewallpaper");
				startActivity(LaunchIntent);
			}
		});
        
        final Button button2 = (Button) findViewById(R.id.button_lego4);
        button2.setOnClickListener(new View.OnClickListener() {
        	@Override
			public void onClick(View v) {
				Intent LaunchIntent = getPackageManager().getLaunchIntentForPackage("com.lego.bricksmore");
				startActivity(LaunchIntent);
			}
		});
        
        final Button button3 = (Button) findViewById(R.id.button_mc);
        button3.setOnClickListener(new View.OnClickListener() {
        	@Override
			public void onClick(View v) {
				Intent LaunchIntent = getPackageManager().getLaunchIntentForPackage("com.mojang.minecraftpe.democom.sketchbookexpress");
				startActivity(LaunchIntent);
			}
		});
        
        final Button button4 = (Button) findViewById(R.id.button_legozoo);
        button4.setOnClickListener(new View.OnClickListener() {
        	@Override
			public void onClick(View v) {
				Intent LaunchIntent = getPackageManager().getLaunchIntentForPackage("dk.spatifo.dublo");
				startActivity(LaunchIntent);
			}
		});
        
        final Button button5 = (Button) findViewById(R.id.button_sketchbook);
        button5.setOnClickListener(new View.OnClickListener() {
        	@Override
			public void onClick(View v) {
				Intent LaunchIntent = getPackageManager().getLaunchIntentForPackage("com.sketchbookexpress");
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
