Running Cyclus on Blue Waters
=============================

1. Login to a MOM node.

   .. code-block:: bash

        $ qsub -I -l walltime=00:30:00 -l nodes=1:ppn=1

2. Load shifter and check if docker image exists on blue waters.

   .. code-block:: bash

        $ module load shifter
        $ getDockerImage lookup arfc/cyclus_blue_waters:latest

   If the image does not exist, pull from docker hub

   .. code-block:: bash

        $ getDockerImage pull arfc/cyclus_blue_waters:latest

3. Run the `cyclus_blue_water.py` script with appropriate options.
   This will generate two files, `cyclus_script.sh` and `pbs_script.pbs`.

   .. table::

    +----------------+-------------------------------+
    |``-h, --help``  |Show help message              |
    +----------------+-------------------------------+
    |``--nodes``     |Number of nodes                |
    +----------------+-------------------------------+
    |``--ppn``       |Processors per node            |
    +----------------+-------------------------------+
    |``--walltime``  |Wall time                      |
    +----------------+-------------------------------+
    |``-o``          |Output type ('sqlite' or 'h5') |
    +----------------+-------------------------------+
    |``--in-dir``    |Inputs directory               |
    +----------------+-------------------------------+
    |``--out-dir``   |Outputs directory              |
    +----------------+-------------------------------+
    |``--log-dir``   |Logs directory                 |
    +----------------+-------------------------------+
    |``--spec-file`` |Path of specification file     |
    +----------------+-------------------------------+


4. Submit the job.

   .. code-block:: bash

        $ qsub pbs_script.pbs

Updating the docker image
=========================

1. Go to repository's home directory and run the following command to build
   the docker image,

   .. code-block:: bash

        $ sudo docker build .

   The last line of output will be as follows,

   Successfully built ``<IMAGE_ID>``

2. Login to docker hub from command line,

   .. code-block:: bash

        $ sudo docker login --username=<USERNAME> --email=<EMAIL>

3. Tag the image using the following command,

   .. code-block:: bash

        $ sudo docker tag <IMAGE_ID> arfc/cyclus_blue_waters:latest

4. Push to docker hub, 

   .. code-block:: bash

        $ sudo docker push arfc/cyclus_blue_waters


