# IST repository
This repository contains all scripts necessary to setup and evaluate an Incremental Step Test (IST). 

### *IST_generator.py*
* Can be used to create machine readable programs for the IST.
* Simply follow the commands displayed in the console and the script returns a machine readable txt-file as well as a visualization of your ramp file. Both files are name after the following pattern, where ... resembles your input parameters. \
  IST-eps_max_...-eps_dot_...-steps_... (.txt or .png)
* The following example has a maximum strain of 1 %, a strain rate of 0.1 % per second and 20 steps \
  (see the example output *IST-eps_max_1.0-eps_dot_0.1-steps_20.txt* in the *examples* folder).

![IST-eps_max_1 0-eps_dot_0 1-steps_20](https://github.com/user-attachments/assets/3073e8c8-895d-45d3-a515-7b6cabbe6e9b)

### *IST_solver.py*
* The IST_solver uses the IST_config.json to read the output of an IST and calculates the Ramberg-Osgood parameters. 
  * *l0*: Enter the initial clip gage length in µm.
  * *d1*, *d2*, *d3*: Provide the specimen diameter in mm.
  * *skip_rows*: Define how many line have to be skipped in the input file (default = 17).
  * *max_strain*: Define the maximum strain (in %) of the performed IST.
  * *youngs_modulus*: Enter Youngs modulus (in MPa).
  * *eval_block*: Enter the IST block you want to evaluate.
  * *txt_path*: Provide the path to the input file. Use double backslashes (\\\\)!
* The input txt-file needs to be in a specified format (see the example input *AOX-LCF-A9-4.txt* in the *examples* folder).
  * The 1st column *zeit* corresponds to the experiment time in seconds.
  * The 2nd column *kraft* corresponds to the measured forces in kN.
  * The 3rd and 5th column (*ext_ist*  and *ext_soll*) are the actual and the target value of the extension.
  * The 4th column *mweg* corresponds to the machine displacement.
  * The 6th column *zyklen* tells the IST block.  
* IST_solver.py outputs a visual analysis of the evaluation for the first block and your defined *eval_block*, as well as a csv-file where the Ramberg-Osgood parameters are stored.

![Evaluation_AOX-LCF-A9-4_block-18](https://github.com/user-attachments/assets/f0c825f2-ba3c-401d-acc1-339c42147762)

### *Run a test*
* After cloning the repo, simply run the script by entering the following command into your console: \
  *python .\IST_solver.py --config_path .\IST_config.json* 
* IST_solver.py and IST_config.json must be in the same folder in order for the command to work like proposed.
* The *txt_path* variable in IST_config will automatically link to the test data in the test folder.
