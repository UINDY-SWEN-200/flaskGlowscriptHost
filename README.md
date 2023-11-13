# Flask Datastore Host

This is a flask based Google DataStore Host. This is very nearly the same code that runs www.glowscript.org at the moment.

The idea is to first get this working with the old auth/Datastore modules but configuring different guest runners.

Then we'll factor out editing/storage to be more modular.

You can run this host app, and the two guest apps in code spaces.

* type `docker compose up` in a terminal window
* Note the URL of the app.
* Edit the .env file of the WASM guest to match this URL
* Edit the `untrusted/run.html` file of the RS guest to match this URL
* Launch the rapydscript guest, and the WASM guest in separate code spaces
* Note the URL of each of these apps
* In the .flaskenv file, set PUBLIC_RUNNER_GUEST_URL and PUBLIC_WASM_GUEST_URL


What We Accomplished:
1) deactivated ace editor in file ide.js line 1440
2) imported monaco editor in file ide.js line 1440
3) Added a route in file routes.py line 124
4) got intellisence to work in file index.html line 345
5) partial work done with saving (i.e. refreshing page and code still being there) using localStorage... change it please, in file ide.js 1450 and file routes.py line 124
6) PATIENCE IS NUMBER 1 VIRTUE file life.svelte line 2

What Needs to be Accomplished:
1) Saving the code **CRITICAL IMPORTANCE**
2) Having code load in when opened
3) test that the relationship with runner is good