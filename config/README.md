# NEMO_II
NEMO_II Repository

# About This Directory
This directory is designed to hold the configuration files for your instance of NEMO. 

# Readable configuration files
1) Name your file config.json
2) The file needs to have the following information: <br/>
  PORT - port number for the database server, for MySQL, this is typically 3306 <br/>
  MySQL USER NAME - user name to access the database <br/>
  PASSWORD - password to access the database <br/>
  DATABASE - name of the database to access <br/>
  DATA - local path from NEMO's root directory to the data file <br/>
  SCHEMA - local path from NEMO's root directory to the file describing the schema of the data <br/>
  CLASS - String with the class to classify.
  
# Recent Updates
1) The config file now includes the local path to the data and data schema files in the data directory <br/>
2) Uses JSON technology instead of flat text files. <br/>

# To-Do
Several updates to the nature of config files are planned/under consideration. As updates are completed, this README will be updated accordingly.
