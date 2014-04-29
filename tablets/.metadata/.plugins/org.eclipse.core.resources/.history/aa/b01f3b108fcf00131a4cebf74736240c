package com.example.movielist0;

import java.io.File;
import java.util.Arrays;
import java.util.List;

import com.example.movielist0.R;

import android.app.Activity;
import android.content.ClipData;
import android.content.Intent;
import android.media.AudioManager;
import android.media.MediaPlayer;
import android.net.Uri;
import android.os.Bundle;
import android.view.DragEvent;
import android.view.Menu;
import android.view.View;
import android.view.View.DragShadowBuilder;
import android.view.View.OnDragListener;
import android.widget.AdapterView;
import android.widget.GridView;

public class MainActivity extends Activity {

	private List<String> film = Arrays.asList("BAMSE_4.Title1.mp4",
			"BUILT_TO_BE_WILD_SCN.Title5.mp4", "DVDVOLUME.Title1.mp4",
			"DVD_FILMPERLER.Title1.mp4", "MW60EZM1.Title1.mp4",
			"POSTMAN_PAT.Title8.mp4", "TT AND THE SNOW.Title2.mp4",
			"THOMAS.Title7.mp4");

	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);

		MediaPlayer mediaPlayer = new MediaPlayer();
		mediaPlayer.setAudioStreamType(AudioManager.STREAM_MUSIC);

		final ImageAdapter movieAdapter = new ImageAdapter(this);
		final GridView movies = (GridView) findViewById(R.id.movies);
		movies.setAdapter(movieAdapter);

		final ChoiceAdapter choiceAdapter = new ChoiceAdapter(this);
		final GridView choices = (GridView) findViewById(R.id.choices);
		choices.setAdapter(choiceAdapter);

		movies.setOnItemLongClickListener(new AdapterView.OnItemLongClickListener() {
			@Override
			public boolean onItemLongClick(AdapterView<?> parent, View view,
					int position, long id) {

				ClipData data = ClipData.newPlainText("" + position, "");
				DragShadowBuilder shadowBuilder = new View.DragShadowBuilder(
						view);
				view.startDrag(data, shadowBuilder, view, 0);
				view.setVisibility(View.INVISIBLE);
				System.out.println(data);
				System.out.println(position);
				return true;
			}
		});

		movies.setOnItemClickListener(new AdapterView.OnItemClickListener() {

			@Override
			public void onItemClick(AdapterView<?> parent, View view,
					int position, long id) {

				Intent intent = new Intent();
				intent.setAction(android.content.Intent.ACTION_VIEW);
				File file = new File("/storage/emulated/0/Movies/"
						+ film.get(position));
				intent.setDataAndType(Uri.fromFile(file), "video/*");
				startActivity(intent);

			}
		});

		findViewById(R.id.choices).setOnDragListener(new OnDragListener() {

			@Override
			public boolean onDrag(View v, DragEvent event) {

				boolean result = true;

				// Defines a variable to store the action type for the incoming
				// event
				View dropped = (View) event.getLocalState();
				// String pos = event.getClipData().getDescription().toString();

				// Handles each of the expected events
				switch (event.getAction()) {

				case DragEvent.ACTION_DRAG_STARTED:
					// no action necessary
					break;
				case DragEvent.ACTION_DRAG_ENTERED:
					// no action necessary
					break;
				case DragEvent.ACTION_DRAG_EXITED:
					// no action necessary
					break;
				case DragEvent.ACTION_DROP:
					if (event.getLocalState() == v) {
						result = false;
					}

					// handle the dragged view being dropped over a drop view

					// System.out.println(pos);
					// dropped.setVisibility(View.VISIBLE);

					break;
				case DragEvent.ACTION_DRAG_ENDED:

					dropped.setVisibility(View.VISIBLE);
					break;
				default:
					break;
				}
				return result;
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
