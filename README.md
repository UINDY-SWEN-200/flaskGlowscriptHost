# Flask Host

This is a flask based host that can use Google DataStore or MongoDB to store user programs and folders. 

This is very nearly the same code that runs www.glowscript.org except it uses a translation layer between the application and the database.

You can run this host app, and the two guest apps in code spaces.

* type `docker compose up` in a terminal window
* Note the URL of the app.
* Edit the .env file of the WASM guest to match this URL
* Edit the `untrusted/run.html` file of the RS guest to match this URL
* Launch the rapydscript guest, and the WASM guest in separate code spaces
* Note the URL of each of these apps
* In the .flaskenv file, set PUBLIC_RUNNER_GUEST_URL and PUBLIC_WASM_GUEST_URL

## Editor Changes/Status

Improvements were made by the Fall 2023 SWEN-200 class at UIndy. 

What They Accomplished:
1) deactivated ace editor in file ide.js line 1440
2) imported monaco editor in file ide.js line 1440
3) Added a route in file routes.py line 124
4) got intellisence to work in file index.html line 345
5) partial work done with saving (i.e. refreshing page and code still being there) using localStorage... change it please, in file ide.js 1450 and file routes.py line 124 -- Finished this in line 1440 in ide.js
6) PATIENCE IS NUMBER 1 VIRTUE file life.svelte line 2

What Needs to be Accomplished:
1) Saving the code **CRITICAL IMPORTANCE** -- This was Finished
2) Having code load in when opened -- This was Finished
3) Getting the right language to load into the editor.
4) test that the relationship with runner is good

## LoadURL Changes/Status

Sprint One - LoadURL Branch

Accomplished - Made pages.load in ide.js which can load code from a URL by using the following route "/user/([^/]+)/folder/([^/]+)/program/([^/]+)/loadURL/(.+)$". This route can also be found in the router().

Status - The program can currently take a URL and run code from the URL.

Next Step - Take code from Google Drive and run it. Start by making a new route in router() for loading code from Google Drive. Make code that you load from Google Drive or using loadURL go into either the database or Google Drive.

Next Next Step - Be able to save, edit, and run code that you load from Google Drive and loadURL

