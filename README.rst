Running Cyclus on Blue Waters
=============================

1. Login to a MOM node and lookup the docker image. Pull the image from
   docker hub if not present.

   .. code-block:: bash

        $ qsub -I -l walltime=00:30:00 -l nodes=1:ppn=1
        $ module load shifter
        $ getDockerImage lookup adityapb/rickshaw:bw
        $ getDockerImage pull adityapb/rickshaw:bw

2. Run the `cyclus_blue_water.py` script with appropriate options (`--help` for help).

3. Submit the job.

   .. code-block:: bash

        $ qsub pbs_script.pbs

