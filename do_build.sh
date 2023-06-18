gcloud builds submit --tag us.gcr.io/glowscript-py38/flaskdstorehost .
gcloud run deploy flaskdstorehost --image us.gcr.io/glowscript-py38/flaskdstorehost
