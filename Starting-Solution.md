# Starting the Solution
Here is the order in which you need to run things to test this solution out.

## Start the Backend first

1. Start the Backend Server using the following commands from a Terminal Window

```
    cd ./backend
    python main.py
```
2. Open the Browser and navigate to http://localhost:8000/docs and you will see the Swagger UI for the backend. Hit the /health endpoint to make sure it's working.


## Now start the frontend, with uses Node.

1. Change to the root directory and run the following command.
```
   npx http-server -p 3000
```
 
2. Open your browser and navigate to http://localhost:3000/single-page-report.html