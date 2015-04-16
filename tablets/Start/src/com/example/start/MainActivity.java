package com.example.start;

import android.app.Activity;
import android.content.Intent;
import android.media.AudioManager;
import android.media.MediaPlayer;
import android.os.Bundle;
import android.view.Menu;
import android.view.View;
import android.widget.Button;

public class MainActivity extends Activity {
	
	Boolean hclicked = false;
	Boolean fclicked = false;
	Boolean aclicked = false;
	

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        final MediaPlayer mpa = MediaPlayer.create(this, R.raw.apps);
        final MediaPlayer mph = MediaPlayer.create(this, R.raw.historier);
        final MediaPlayer mpf = MediaPlayer.create(this, R.raw.film);
        
        
        final Button buttonA = (Button) findViewById(R.id.button_a);
        
        
        
        
        buttonA.setOnClickListener(new View.OnClickListener() {
        	@Override
			public void onClick(View v) {
        		if (aclicked){      		
        			Intent LaunchIntent = getPackageManager().getLaunchIntentForPackage("com.example.apps");
					startActivity(LaunchIntent);
					
        		} else {
        			mpa.setAudioStreamType(AudioManager.STREAM_MUSIC);
        			mpa.start();
        			aclicked = true;
        			
        		}
			}
		});
        
        final Button buttonE = (Button) findViewById(R.id.button_h);
        buttonE.setOnClickListener(new View.OnClickListener() {
        	@Override
			public void onClick(View v) {
	        	if (hclicked) {
					Intent LaunchIntent = getPackageManager().getLaunchIntentForPackage("com.example.historie");
					startActivity(LaunchIntent);
        		} else {
        			mph.setAudioStreamType(AudioManager.STREAM_MUSIC);
        			mph.start();
        			hclicked = true;
        		}
			}
		});
        
        final Button buttonF = (Button) findViewById(R.id.button_f);
        buttonF.setOnClickListener(new View.OnClickListener() {
        	@Override
			public void onClick(View v) {
        		if (fclicked) {
					Intent LaunchIntent = getPackageManager().getLaunchIntentForPackage("com.example.agechoice_movies");
					startActivity(LaunchIntent);
        		}else {
        			mpf.setAudioStreamType(AudioManager.STREAM_MUSIC);
        			mpf.start();
        			fclicked = true;
        		}
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
