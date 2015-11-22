# codered
Code Red hackathon
Step 1
--------
python ssl-audit.py top-1m.csv 1>result.csv 2>error.txt

Input File - top-1m.csv
Output File- result.csv
Error report- error.txt

default certificate: dummycert.pem (can be found in attached repository)

Step 2
--------
python processOutputToJSON.py result.csv result.json

Input File - result.csv
Output File- result.json

Step3
--------
Copy the ScreenRender directory (ASP.Net application) to any drive of web server.
Create an application in IIS. Set the Application Pool as .Net V4.5.
Configure the Virtual Directory to point to the folder where the application resides in the physical path.
Restart the IIS Manager.
Access https://<dns>/<virtualdirectory> to see the results
