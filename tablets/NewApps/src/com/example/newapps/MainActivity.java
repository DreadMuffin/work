package com.example.newapps;
 
import java.util.List;
 



import android.app.Activity;
import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.content.pm.PackageManager;
import android.content.pm.ResolveInfo;
import android.os.Bundle;
import android.util.Log;
import android.view.Gravity;
import android.view.View;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemClickListener;
import android.widget.GridView;
 
public class MainActivity extends Activity {
 
    PackageManager myPackageManager;
 
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        
        myPackageManager = getPackageManager();
 
        Intent intent = new Intent(Intent.ACTION_MAIN, null);
        intent.addCategory(Intent.CATEGORY_LAUNCHER);
        List<ResolveInfo> appIntentList = getPackageManager()
                .queryIntentActivities(intent, 0);
        
        GridView gridview = (GridView) findViewById(R.id.apps);

        
        for (ResolveInfo resolveInfo : appIntentList) {
        	   System.out.println("New Launcher Found: " + resolveInfo.activityInfo.packageName);
        	}
        
        
        System.out.println(appIntentList.toString());
 
        gridview.setAdapter(new ImageAdapter(this, appIntentList));
        
        gridview.setOnItemClickListener(new OnItemClickListener() {
 
            @Override
            public void onItemClick(AdapterView<?> parent, View view,
                    int position, long id) {
                ResolveInfo cleckedResolveInfo = (ResolveInfo) parent
                        .getItemAtPosition(position);
                ActivityInfo clickedActivityInfo = cleckedResolveInfo.activityInfo;
 
                Intent intent = new Intent(Intent.ACTION_MAIN);
                intent.addCategory(Intent.CATEGORY_LAUNCHER);
                intent.setClassName(
                        clickedActivityInfo.applicationInfo.packageName,
                        clickedActivityInfo.name);
                intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK
                        | Intent.FLAG_ACTIVITY_RESET_TASK_IF_NEEDED);
                startActivity(intent);
            }
 
        });
 
    }
}