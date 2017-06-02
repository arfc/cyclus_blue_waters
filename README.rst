Running Cyclus on Blue Waters
=============================

Imagine you have a cyclus simulation that you would like to run many times
with varied parameters or agents. You can use this workflow to generate 
an input file for each desired simulation and to run those input files 
simultaneously on the Blue Waters supercomputer.

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

    +----------------+--------------------------------------------------+
    |``-h, --help``  |Show help message                                 |
    +----------------+--------------------------------------------------+
    |``--nodes``     |Number of nodes                                   |
    +----------------+--------------------------------------------------+
    |``--ppn``       |Processors per node                               |
    +----------------+--------------------------------------------------+
    |``--walltime``  |Max time your job can run (hours:minutes:seconds) |
    +----------------+--------------------------------------------------+
    |``-o``          |Output type ('sqlite' or 'h5')                    |
    +----------------+--------------------------------------------------+
    |``--in-dir``    |Inputs directory                                  |
    +----------------+--------------------------------------------------+
    |``--out-dir``   |Outputs directory                                 |
    +----------------+--------------------------------------------------+
    |``--log-dir``   |Logs directory                                    |
    +----------------+--------------------------------------------------+
    |``--spec-file`` |Path of specification file*                       |
    +----------------+--------------------------------------------------+

   *\* Specification files are Rickshaw input files in which you can define
   constraints for generation*

4. Submit the job.

   .. code-block:: bash

        $ qsub pbs_script.pbs

Updating the docker image
=========================

The docker image needs to be updated if the cyclus or cycamore installation
in the image is to be updated.

The docker image will be automatically updated in docker hub when a commit is 
pushed to cyclus or cycamore.

As rickshaw doesn't have an automated build, to update the rickshaw installation
in the docker image, the image needs to be manually updated.

To manually update the image, go to the docker hub `page <https://hub.docker.com/r/arfc/cyclus_blue_waters/>`_, 
then go to *Build Settings* and trigger a build.

