package com.example.movielisthis;

import com.example.movielisthis.R;

import android.app.Activity;
import android.app.ActionBar.LayoutParams;
import android.content.Context;
import android.graphics.drawable.BitmapDrawable;
import android.os.Bundle;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.GridView;
import android.widget.PopupWindow;

public class MainActivity extends Activity {
	Button button_1;

	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);

		final ImageAdapter movieAdapter = new ImageAdapter(this);
		final GridView movies = (GridView) findViewById(R.id.movies);
		movies.setAdapter(movieAdapter);

		movies.setOnItemClickListener(new AdapterView.OnItemClickListener() {

			@Override
			public void onItemClick(AdapterView<?> parent, View view,
					int position, long id) {
				if (position != 0 && position != 5) {
					if (position > 5) {
						position--;
					}
					initiatePopupWindow(position);
				}

			}
			
		});
	}

	private PopupWindow pwindo;

	private void initiatePopupWindow(int i) {
		try {
			// We need to get the instance of the LayoutInflater
			
			LayoutInflater inflater = (LayoutInflater) MainActivity.this
					.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
			
			

			switch (i) {
			case 1:
				View layout = inflater.inflate(R.layout.popup1,
						(ViewGroup) findViewById(R.id.popup_element1));
				pwindo = new PopupWindow(layout, LayoutParams.MATCH_PARENT,
						LayoutParams.MATCH_PARENT, true);
				pwindo.setBackgroundDrawable(new BitmapDrawable(getResources(),""));
				pwindo.showAtLocation(layout, Gravity.CENTER, 0, 0);
				


				break;

			case 2:
				View layout2 = inflater.inflate(R.layout.popup2,
						(ViewGroup) findViewById(R.id.popup_element2));
				pwindo = new PopupWindow(layout2, LayoutParams.MATCH_PARENT,
						LayoutParams.MATCH_PARENT, true);
				pwindo.setBackgroundDrawable(new BitmapDrawable(getResources(),""));
				pwindo.showAtLocation(layout2, Gravity.CENTER, 0, 0);

				break;
			case 3:
				View layout3 = inflater.inflate(R.layout.popup3,
						(ViewGroup) findViewById(R.id.popup_element3));
				pwindo = new PopupWindow(layout3, LayoutParams.MATCH_PARENT,
						LayoutParams.MATCH_PARENT, true);
				pwindo.setBackgroundDrawable(new BitmapDrawable(getResources(),""));
				pwindo.showAtLocation(layout3, Gravity.CENTER, 0, 0);
				break;
			case 4:
				View layout4 = inflater.inflate(R.layout.popup4,
						(ViewGroup) findViewById(R.id.popup_element4));
				pwindo = new PopupWindow(layout4, LayoutParams.MATCH_PARENT,
						LayoutParams.MATCH_PARENT, true);
				pwindo.setBackgroundDrawable(new BitmapDrawable(getResources(),""));
				pwindo.showAtLocation(layout4, Gravity.CENTER, 0, 0);
				break;
			case 5:
				View layout5 = inflater.inflate(R.layout.popup5,
						(ViewGroup) findViewById(R.id.popup_element5));
				pwindo = new PopupWindow(layout5, LayoutParams.MATCH_PARENT,
						LayoutParams.MATCH_PARENT, true);
				pwindo.setBackgroundDrawable(new BitmapDrawable(getResources(),""));
				pwindo.showAtLocation(layout5, Gravity.CENTER, 0, 0);
				break;
			case 6:
				View layout6 = inflater.inflate(R.layout.popup6,
						(ViewGroup) findViewById(R.id.popup_element6));
				pwindo = new PopupWindow(layout6, LayoutParams.MATCH_PARENT,
						LayoutParams.MATCH_PARENT, true);
				pwindo.setBackgroundDrawable(new BitmapDrawable(getResources(),""));
				pwindo.showAtLocation(layout6, Gravity.CENTER, 0, 0);
				break;
			case 7:
				View layout7 = inflater.inflate(R.layout.popup7,
						(ViewGroup) findViewById(R.id.popup_element7));
				pwindo = new PopupWindow(layout7, LayoutParams.MATCH_PARENT,
						LayoutParams.MATCH_PARENT, true);
				pwindo.setBackgroundDrawable(new BitmapDrawable(getResources(),""));
				pwindo.showAtLocation(layout7, Gravity.CENTER, 0, 0);
				break;
			case 8:
				View layout8 = inflater.inflate(R.layout.popup8,
						(ViewGroup) findViewById(R.id.popup_element8));
				pwindo = new PopupWindow(layout8, LayoutParams.MATCH_PARENT,
						LayoutParams.MATCH_PARENT, true);
				pwindo.setBackgroundDrawable(new BitmapDrawable(getResources(),""));
				pwindo.showAtLocation(layout8, Gravity.CENTER, 0, 0);
				break;
			case 9:
				View layout9 = inflater.inflate(R.layout.popup9,
						(ViewGroup) findViewById(R.id.popup_element9));
				pwindo = new PopupWindow(layout9, LayoutParams.MATCH_PARENT,
						LayoutParams.MATCH_PARENT, true);
				pwindo.setBackgroundDrawable(new BitmapDrawable(getResources(),""));
				pwindo.showAtLocation(layout9, Gravity.CENTER, 0, 0);
				break;
			case 10:
				View layout10 = inflater.inflate(R.layout.popup10,
						(ViewGroup) findViewById(R.id.popup_element10));
				pwindo = new PopupWindow(layout10, LayoutParams.MATCH_PARENT,
						LayoutParams.MATCH_PARENT, true);
				pwindo.setBackgroundDrawable(new BitmapDrawable(getResources(),""));
				pwindo.showAtLocation(layout10, Gravity.CENTER, 0, 0);
				break;
			case 11:
				View layout11 = inflater.inflate(R.layout.popup11,
						(ViewGroup) findViewById(R.id.popup_element11));
				pwindo = new PopupWindow(layout11, LayoutParams.MATCH_PARENT,
						LayoutParams.MATCH_PARENT, true);
				pwindo.setBackgroundDrawable(new BitmapDrawable(getResources(),""));
				pwindo.showAtLocation(layout11, Gravity.CENTER, 0, 0);
				break;

			case 12:
				i = 12;
				View layout12 = inflater.inflate(R.layout.popup12,
						(ViewGroup) findViewById(R.id.popup_element12));
				pwindo = new PopupWindow(layout12, LayoutParams.MATCH_PARENT,
						LayoutParams.MATCH_PARENT, true);
				pwindo.setBackgroundDrawable(new BitmapDrawable(getResources(),""));
				pwindo.showAtLocation(layout12, Gravity.CENTER, 0, 0);
				break;
			case 13:
				i = 13;
				View layout13 = inflater.inflate(R.layout.popup13,
						(ViewGroup) findViewById(R.id.popup_element13));
				pwindo = new PopupWindow(layout13, LayoutParams.MATCH_PARENT,
						LayoutParams.MATCH_PARENT, true);
				pwindo.setBackgroundDrawable(new BitmapDrawable(getResources(),""));
				pwindo.showAtLocation(layout13, Gravity.CENTER, 0, 0);
				break;

			case 14:
				i = 14;
				View layout14 = inflater.inflate(R.layout.popup14,
						(ViewGroup) findViewById(R.id.popup_element14));
				pwindo = new PopupWindow(layout14, LayoutParams.MATCH_PARENT,
						LayoutParams.MATCH_PARENT, true);
				pwindo.setBackgroundDrawable(new BitmapDrawable(getResources(),""));
				pwindo.showAtLocation(layout14, Gravity.CENTER, 0, 0);
				break;

			case 15:
				i = 15;
				View layout15 = inflater.inflate(R.layout.popup15,
						(ViewGroup) findViewById(R.id.popup_element15));
				pwindo = new PopupWindow(layout15, LayoutParams.MATCH_PARENT,
						LayoutParams.MATCH_PARENT, true);
				pwindo.setBackgroundDrawable(new BitmapDrawable(getResources(),""));
				pwindo.showAtLocation(layout15, Gravity.CENTER, 0, 0);
				break;

			case 16:
				i = 16;
				View layout16 = inflater.inflate(R.layout.popup16,
						(ViewGroup) findViewById(R.id.popup_element16));
				pwindo = new PopupWindow(layout16, LayoutParams.MATCH_PARENT,
						LayoutParams.MATCH_PARENT, true);
				pwindo.setBackgroundDrawable(new BitmapDrawable(getResources(),""));
				pwindo.showAtLocation(layout16, Gravity.CENTER, 0, 0);
				break;

			}

		} catch (Exception e) {
			e.printStackTrace();
		}
	}



}
