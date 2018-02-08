# Current LD-R Configuration

In order to import and integrate the triple store that is hosted by STARDOG, numerous adjustments were made to the configuration files of LD-R. These modified configuration files can be found in ld-r/configs directory. 

# Instructions for Building and Configuring LD-R

## Running LD-R
1. First, make sure that the terminal is in 'ld-r' directory.
(It is recommended to have no spaces in file path)

2. Build/Run LD-R either dev or build mode with ONE OF the following commands:

### Development Mode

    npm run dev (no need to add 'dev:windows' unless there is a problem)
    runs on port 4000
    quicker to load

### Build Mode

    runs on port 3000 or 3001
    npm run build:windows
        optimizes (minifies + handles dependencies + removes duplicates, etc) and runs JS files


## Configuration
**Note**: After each config change, LD-R must be shut down and run again.

Demo database for LD-R config:

    C:\ld-r\plugins\dynamicConfiguration\schema\configs.ttl

### General Configuration

LD-R configs directory:
    
    C:\ld-r\configs\general.js

### Server Configuration

    C:\ld-r\configs\server.js
    
for configuring stardog and database(s) it contains ():

	    sparqlEndpoint: {
        'generic': {
            // this must be stardog port (e.g., 5820), and the database name (e.g., sr)
            //Stardog note: sometimes you need to use a path like '/annex/MY_DATABASE_NAME_IN_STARDOG/sparql/query' for update queries
            host: 'localhost', port: 5820, path: '/annex/sr/sparql/query', graphName: 'default', endpointType: 'stardog', useReasoning: 1
        },
        //Note: if graphName is not specified, the identifer used for configuration will be used as graphName
        //Example config for connecting to a Stardog triple store
        'http://localhost:5820/testDB/query': {
            host: 'localhost', port: 5820, path: '/testDB/query', graphName: 'default', endpointType: 'stardog', useReasoning: 1
        },
        //Example for connecting to a Virtuoso triple store
        'http://live.dbpedia.org/sparql': {
            host: 'dbpedia.org', port: 80, path: '/sparql', graphName: 'default', endpointType: 'virtuoso'
        },
        //Example for connecting to a ClioPatria triple store
        'http://localhost:3020/sparql/': {
            host: 'localhost', port: 3020, path: '/sparql/', endpointType: 'ClioPatria'
        }
    },   
    
# User Authentication

For authentication...
 
1 - Add user schema file to triple store at:

    C:\ld-r\plugins\authentication\schema\users.ttl

2 - Edit 'configs\general.js' as follows to enable authentication:

    //will prevent access if not logged in
    enableAuthentication: 1,
    //graph that stores users data, must be loaded beforehand
    authDatasetURI: ['http://ld-r.org/users'],
    //will allow super users to confirm and activate regiastered users
    enableUserConfirmation: 1,


Troubleshooting in case of user signup/login problems:

- Remove the defaultGraph from the generic config (by Ali)
    
