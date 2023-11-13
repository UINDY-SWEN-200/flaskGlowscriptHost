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



Sprint One - LoadURL Branch

Accomplished - Made pages.load in ide.js which can load code from a URL by using the following route "/user/([^/]+)/folder/([^/]+)/program/([^/]+)/loadURL/(.+)$". This route can also be found in the router().


Status - The program can currently take a URL and run code from the URL.


Next Step - Take code from Google Drive and run it.

