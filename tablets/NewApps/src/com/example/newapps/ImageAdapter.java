package com.example.newapps;
 
import java.util.List;
import android.content.Context;
import android.content.pm.PackageManager;
import android.content.pm.ResolveInfo;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.GridView;
import android.widget.ImageView;
 
public class ImageAdapter extends BaseAdapter {
 
    private Context myContext;
    private List<ResolveInfo> MyAppList;
    PackageManager myPackageManager;
 
    ImageAdapter(Context c, List<ResolveInfo> appIntentList) {
        myContext = c;
        MyAppList = appIntentList;
        myPackageManager = c.getPackageManager();
    }
 
    @Override
    public int getCount() {
        return MyAppList.size();
    }
 
    @Override
    public Object getItem(int position) {
        return MyAppList.get(position);
    }
 
    @Override
    public long getItemId(int position) {
        return position;
    }
 
    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
 
        ImageView imageView;
        if (convertView == null) {
            imageView = new ImageView(myContext);
            imageView.setLayoutParams(new GridView.LayoutParams(85, 85));
            imageView.setScaleType(ImageView.ScaleType.CENTER_CROP);
            imageView.setPadding(8, 8, 8, 8);
        } else {
            imageView = (ImageView) convertView;
        }
 
        ResolveInfo resolveInfo = MyAppList.get(position);
        imageView.setImageDrawable(resolveInfo.loadIcon(myPackageManager));
 
        return imageView;
 
    }
 
}