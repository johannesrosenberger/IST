# IST repository
This repository contains all scripts necessary to setup and evaluate an Incremental Step Test (IST). 

IST_generator.py
* Can be used to create machine readable programs for the IST.
* Simply follow the commands displayed in the console and the script returns a machine readable txt-file as well as a visualization of your ramp file.

![Screenshot of a generated IST program](https://private-user-images.githubusercontent.com/94892196/386638255-d5c6abaf-0917-4730-a4c7-afcf286d1a3e.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MzE2ODExOTcsIm5iZiI6MTczMTY4MDg5NywicGF0aCI6Ii85NDg5MjE5Ni8zODY2MzgyNTUtZDVjNmFiYWYtMDkxNy00NzMwLWE0YzctYWZjZjI4NmQxYTNlLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDExMTUlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQxMTE1VDE0MjgxN1omWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWNhMzQ4NGIzZGNkZjIyYjY3NTQwODY0YjM1MTMwYTEwYTczYWM2OTIxMmE0MDZlMjhmYzQ3Yzg1MmVhMzgzYjYmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.s7M9zId6OH_H0janQvGp4f_Q4DY5tbVwNFIDDGU79u4)

IST_solver.py
* The IST_solver uses the IST_config.json to read the output of an IST. The file needs to be in a specified format (see example files).
  * *l0*: Enter the initial clip gage length in µm.
  * *d1*, *d2*, *d3*: Provide the specimen diameter in mm.
  * *skip_rows*: Define how many line have to be skipped in the input file (default = 17).
  * *max_strain*: Define the maximum strain (in %) of the performed IST.
  * *youngs_modulus*: Enter Youngs modulus (in MPa).
  * *eval_block*: Enter the IST block you want to evaluate.
  * *txt_path*: Provide the path to the input file. Use double backslashes (\\\\)!
* To start the script, simpy enter the following command into your console: \
  *python .\IST_solver.py --config_path .\IST_config.json* 
* IST_solver.py and IST_config.json must be in the same folder in order for the command to work like proposed. Of course you can also store the config file somewhere else.
* IST_solver.py outputs a visual analysis of the evaluation for the first block and your defined *eval_block*.

