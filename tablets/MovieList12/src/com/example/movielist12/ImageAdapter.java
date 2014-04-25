package com.example.movielist12;

import java.util.ArrayList;

import com.example.movielist12.R;

import android.app.Activity;
import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ImageView;
import android.widget.TextView;

public class ImageAdapter extends BaseAdapter {
	private Context mContext;

	public ArrayList<View> movies = new ArrayList<View>();
	Activity activity;

	// references to our texts
	private String[] mTextsIds = { "Eventyret om den vidunderlige kartoffel",
			"Danske filmperler for børn", "Ponyo", "Timmy-Tid", "Ninjaturtles",
			"Animal Agents" };

	// references to our images
	private Integer[] mThumbIds = { R.drawable.kartoffel, R.drawable.mis,
			R.drawable.ponyo, R.drawable.timmy, R.drawable.turtles,
			R.drawable.animal };

	public ImageAdapter(Context c) {
		mContext = c;

	}

	/**
	 * @param mContext
	 * @param mTextsIds
	 * @param mThumbIds
	 * @param movies
	 */
	public ImageAdapter(Context mContext, String[] mTextsIds,
			Integer[] mThumbIds, ArrayList<View> movies, Activity activity) {
		super();
		this.mContext = mContext;
		this.mTextsIds = mTextsIds;
		this.mThumbIds = mThumbIds;
		this.movies = movies;
		this.activity = activity;
	}

	public int getCount() {
		return mThumbIds.length;
	}

	public Object getItem(int position) {
		return null;
	}

	// create a new ImageView for each item referenced by the Adapter
	/*
	 * public View getView(int position, View convertView, ViewGroup parent) {
	 * ImageView imageView; if (convertView == null) { // if it's not recycled,
	 * initialize some // attributes imageView = new ImageView(mContext);
	 * imageView.setLayoutParams(new GridView.LayoutParams(85, 85));
	 * imageView.setScaleType(ImageView.ScaleType.CENTER_CROP);
	 * imageView.setPadding(8, 8, 8, 8); } else { imageView = (ImageView)
	 * convertView; }
	 * 
	 * imageView.setImageResource(mThumbIds[position]); return imageView; }
	 */

	public long getItemId(int position) {
		return 0;
	}

	public View getView(int position, View convertView, ViewGroup parent) {
		View v;

		if (convertView == null) { // if it’s not recycled, initialize some
									// attributes
			LayoutInflater li = (LayoutInflater) mContext
					.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
			v = li.inflate(R.layout.grid_item, null);
			TextView tv = (TextView) v.findViewById(R.id.icon_text);
			tv.setText(mTextsIds[position]);
			ImageView iv = (ImageView) v.findViewById(R.id.icon_image);
			// iv.setLayoutParams(new GridView.LayoutParams(85, 85));
			// iv.setScaleType(ImageView.ScaleType.CENTER_CROP);
			iv.setPadding(8, 8, 8, 8);
			iv.setImageResource(mThumbIds[position]);
		} else {
			v = (View) convertView;
		}
		return v;
	}

}
