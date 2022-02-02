# FactFindr

## Directions for Setup:

This assumes you have already setup the requirements for JumboDB
and have credentials (c3creds.json).

Activate the python (conda) environment you installed JumboDB to. 

Before running the server, make sure you have set the environment
variable `c3creds`. You can do this in MacOS with 
```
export c3creds=</path/to/c3creds.json>
```
or if you’re on Windows:
```
set c3creds=</path/to/c3creds.json>
```

## Running the server

After setting the environment variable and ensuring that you're
in the correct environment, navigate to the home directory of
the folder, and type either:
```
python app.py
```
or 
```
python3 app.py
```
(Depending on how your environment is setup at least one should
work. Just use whichever one doesn't cause an error.)

After that, you should be able to naviagate to the URL address
`http://127.0.0.1:5060/`, and access the site.
    