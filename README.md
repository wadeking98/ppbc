# PPBC  
## Patient Portal British Columbia  
The PPBC project was developed by Wade King under the supervision of Quartech 
Systems Ltd. PPBC is designed to allow users to manage their own health data, 
and allow organizations to easily verify that data.  
PPBC uses Hyperledger Aries for a verifyable credential library and
von-network as a distributed ledger.

You must have node, npm, python3 and pip3 installed and accessable on
your path before you can run PPBC

to download and install PPBC navigate to your home directory and run the 
following commands
> git clone https://github.com/wadeking98/ppbc.git  
> git clone https://github.com/bcgov/von-network.git von  

Once both have finished downloading, change directories to the folder titled
ppbc and run the following commands
> ./manage build  
> ./manage start  

The build command will take some time, but after it completes building without
any errors, it does not need to be built again

navigate to http://localhost:8000 and you should see PPBC up and running.

to kill PPBC press ctrl+c in the terminal running the PPBC server and then run
the following command
> ./manage kill  

