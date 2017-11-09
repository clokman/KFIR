# SETUP INSTRUCTIONS

## STARDOG:
1. Installation: Follow instructions at: kadvgraaf...
2. Set stardog to run as admin  
3. Run stardog with the following command (admin powershell)
```
stardog-admin server start --disable-security
```

4. Set up a triple store with these options:
sameAs reasoning: full
strict          : off
search          : enable
spatial         : on



### Additional Stardog command line

Add data (never worked): 
```
C:\> stardog data add -g <file location> 
```

## LD-R:
1. Do: http://ld-r.org/docs/quickstart.html
2. In configs/server.js, add the in the following code (i.e., the line with the word "annex" in it instead of the default generic SPARQL endpoint entry, which is commented out), with a valid Stardog server name (in this example, "sr3" is the Stardog server name):
``` 
   sparqlEndpoint: {
    'generic': {
       // host: 'localhost', port: 8890, path: '/sparql', endpointType: 'virtuoso'
          host: 'localhost', port: 5820, path: '/annex/sr3/sparql/query', endpointType: 'Stardog'

        },
        ...

```

3. Enable WYSIWYQ
Add these to the file's reactor config:

```
displayQueries
```