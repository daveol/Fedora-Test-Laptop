==Avocado upload script and daemon config==

The script can be used together with the configuration file to create an uploading service.

* ```avocado-upload.py``` - watches the ```avocado/job-results/``` dir for new results with 
  Pyinotify. These results are zipped and uploaded to a certain location (now a dir on localhost) 
  using scp. The test name and outcome are extracted using the ```results.json``` file from 
  the Avocado result. These values are stored in json and uploaded with a post to ResultsDB 
  using the Python requests library.
* ```results-watch.service``` - is a systemd configuration file that executes the 
  ```avocado-upload.py``` script at start up by 'testuser'.
  
The configuration file needs to be saved in the ```/lib/systemd/system/``` directory, and a 
user 'testuser' needs to exist, which has the script saved in its home directory. Otherwise, 
the configuration file needs to be altered.

The watched directories and other directories for saving files, or remote locations may need 
to be altered in the script to fit your needs. Note that the link to the complete zipped results 
is stored in ResultsDB's ref_url.
