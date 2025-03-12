gcloud builds submit --tag us.gcr.io/glowscript/flaskdstorehost .
gcloud run deploy flaskdstorehost --image us.gcr.io/glowscript/flaskdstorehost
