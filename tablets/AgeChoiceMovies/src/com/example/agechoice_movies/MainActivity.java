package com.example.agechoice_movies;

import android.app.Activity;
import android.content.Intent;
import android.media.AudioManager;
import android.media.MediaPlayer;
import android.os.Bundle;
import android.view.Menu;
import android.view.View;
import android.widget.Button;

import com.example.agechoice_movies.R;

public class MainActivity extends Activity {
	
	Boolean hclicked = false;
	MediaPlayer mph;
	
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        mph = MediaPlayer.create(this, R.raw.ekstrafilm);
        
        final Button buttonA = (Button) findViewById(R.id.Button_nul);
        buttonA.setOnClickListener(new View.OnClickListener() {
        	@Override
			public void onClick(View v) {
				Intent LaunchIntent = getPackageManager().getLaunchIntentForPackage("com.example.movielist0");
				startActivity(LaunchIntent);
				stopMedia(mph);
			}
		});

        final Button buttonB = (Button) findViewById(R.id.Button_tre);
        buttonB.setOnClickListener(new View.OnClickListener() {
        	@Override
			public void onClick(View v) {
				Intent LaunchIntent = getPackageManager().getLaunchIntentForPackage("com.example.movielist7");
				startActivity(LaunchIntent);
				stopMedia(mph);
			}
		});

        final Button buttonC = (Button) findViewById(R.id.Button_syv);
        buttonC.setOnClickListener(new View.OnClickListener() {
        	@Override
			public void onClick(View v) {
				Intent LaunchIntent = getPackageManager().getLaunchIntentForPackage("com.example.movielist3");
				startActivity(LaunchIntent);
				stopMedia(mph);
			}
		});

        final Button buttonD = (Button) findViewById(R.id.Button_ti);
        buttonD.setOnClickListener(new View.OnClickListener() {
        	@Override
			public void onClick(View v) {
				Intent LaunchIntent = getPackageManager().getLaunchIntentForPackage("com.example.movielist10");
				startActivity(LaunchIntent);
				stopMedia(mph);
			}
		});

        final Button buttonE = (Button) findViewById(R.id.Button_tolv);
        buttonE.setOnClickListener(new View.OnClickListener() {
        	@Override
			public void onClick(View v) {
				Intent LaunchIntent = getPackageManager().getLaunchIntentForPackage("com.example.movielist12");
				startActivity(LaunchIntent);
				stopMedia(mph);
			}
		});
        
        
        final Button buttonF = (Button) findViewById(R.id.Button_his);
        buttonF.setOnClickListener(new View.OnClickListener() {
        	@Override
			public void onClick(View v) {
        		if (hclicked){
					Intent LaunchIntent = getPackageManager().getLaunchIntentForPackage("com.example.movielisthis");
					startActivity(LaunchIntent);
					stopMedia(mph);
        		} else {
        			mph.setAudioStreamType(AudioManager.STREAM_MUSIC);
        			mph.start();
        			hclicked = true;
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
    
    public void stopMedia(MediaPlayer m){
    	if (m.isPlaying()){
    		m.stop();
    	}
    }
    
    @Override
    public void onPause(){
    	super.onPause();
        if(mph != null && mph.isPlaying())
            mph.stop();
        finish();
    }
    
    
    
    
}
