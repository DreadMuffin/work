package com.example.historie;

import android.app.Activity;
import android.content.Context;
import android.graphics.drawable.BitmapDrawable;
import android.media.AudioManager;
import android.media.MediaPlayer;
import android.os.Bundle;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.PopupWindow;

public class Historie extends Activity {

	Button button_1;
	Button button_2;
	Button button_3;
	Button resize;
	MediaPlayer mp;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_historie);

		// final Button button = (Button) findViewById(R.id.button_1);

		button_1 = (Button) findViewById(R.id.button_1);
		button_2 = (Button) findViewById(R.id.button_2);
		button_3 = (Button) findViewById(R.id.button_3);

		button_1.setOnClickListener(new View.OnClickListener() {

			@Override
			public void onClick(View v) {
				initiatePopupWindow(1);
			}

		});

		button_2.setOnClickListener(new View.OnClickListener() {

			@Override
			public void onClick(View v) {
				initiatePopupWindow(2);
			}
		});

		button_3.setOnClickListener(new View.OnClickListener() {

			@Override
			public void onClick(View v) {
				initiatePopupWindow(3);
			}
		});

	}

	private PopupWindow pwindo;

	private void initiatePopupWindow(int i) {
		try {

			// We need to get the instance of the LayoutInflater
			LayoutInflater inflater = (LayoutInflater) Historie.this
					.getSystemService(Context.LAYOUT_INFLATER_SERVICE);

			if (i == 1) {
				if (mp != null && mp.isPlaying())
					mp.stop();

				mp = MediaPlayer.create(this, R.raw.elvira);
				mp.setAudioStreamType(AudioManager.STREAM_MUSIC);
				mp.start();

				View layout = inflater.inflate(R.layout.popup1,
						(ViewGroup) findViewById(R.id.popup_element1));
				pwindo = new PopupWindow(layout,
						android.view.ViewGroup.LayoutParams.MATCH_PARENT,
						android.view.ViewGroup.LayoutParams.MATCH_PARENT, true);
				pwindo.setBackgroundDrawable(new BitmapDrawable(getResources(),
						""));
				pwindo.setOutsideTouchable(true);
				pwindo.setFocusable(true);
				pwindo.showAtLocation(layout, Gravity.CENTER, 0, 0);

			} else if (i == 2) {
				if (mp != null && mp.isPlaying())
					mp.stop();

				mp = MediaPlayer.create(this, R.raw.odder);
				mp.setAudioStreamType(AudioManager.STREAM_MUSIC);
				mp.start();

				View layout = inflater.inflate(R.layout.popup2,
						(ViewGroup) findViewById(R.id.popup_element2));
				pwindo = new PopupWindow(layout,
						android.view.ViewGroup.LayoutParams.MATCH_PARENT,
						android.view.ViewGroup.LayoutParams.MATCH_PARENT, true);
				pwindo.setBackgroundDrawable(new BitmapDrawable(getResources(),
						""));
				pwindo.setOutsideTouchable(true);
				pwindo.setFocusable(true);
				pwindo.showAtLocation(layout, Gravity.CENTER, 0, 0);

			} else if (i == 3) {
				if (mp != null && mp.isPlaying())
					mp.stop();

				mp = MediaPlayer.create(this, R.raw.bjorni);
				mp.setAudioStreamType(AudioManager.STREAM_MUSIC);
				mp.start();

				View layout = inflater.inflate(R.layout.popup3,
						(ViewGroup) findViewById(R.id.popup_element3));
				pwindo = new PopupWindow(layout,
						android.view.ViewGroup.LayoutParams.MATCH_PARENT,
						android.view.ViewGroup.LayoutParams.MATCH_PARENT, true);
				
		//		resize = (Button) findViewById(R.id.resize);
				
				
				
				pwindo.setBackgroundDrawable(new BitmapDrawable(getResources(),
						""));
				
				pwindo.showAtLocation(layout, Gravity.CENTER, 0, 0);

				

	/*			resize.setOnClickListener(new Button.OnClickListener() {
											
						initiatePopupWindow(4);
					}
				});*/
			} else {

				View layout = inflater.inflate(R.layout.bjorni,
						(ViewGroup) findViewById(R.id.bjorniimg));
				pwindo = new PopupWindow(layout,
						android.view.ViewGroup.LayoutParams.MATCH_PARENT,
						android.view.ViewGroup.LayoutParams.MATCH_PARENT, true);
				pwindo.setBackgroundDrawable(new BitmapDrawable(getResources(),
						""));
				pwindo.setOutsideTouchable(true);
				pwindo.setFocusable(true);
				pwindo.showAtLocation(layout, Gravity.CENTER, 0, 0);
			}

		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	@Override
	public void onPause() {
		super.onPause();
		if (mp != null && mp.isPlaying())
			mp.stop();
		finish();
	}
	
	
}
