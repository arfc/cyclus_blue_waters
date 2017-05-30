#!/usr/bin/env python
from subprocess import call
import os
import sys
import time
from argparse import ArgumentParser
from textwrap import dedent

CYCLUS_SCRIPT = \
    """
    #!/bin/bash
    cyclus %(in_dir)s/$ALPS_APP_PE.json -o \
            %(out_dir)s/$ALPS_APP_PE.%(out_type)s \
            > %(log_dir)s/out_$ALPS_APP_PE.log
    """

PBS_SCRIPT = \
    """
    #!/bin/bash
    #PBS -l gres=shifter
    #PBS -v UDI=adityapb/rickshaw:bw
    #PBS -l nodes=%(nodes)s:ppn=%(ppn)s:xe
    #PBS -l walltime=%(walltime)s
    export CRAY_ROOTFS=UDI
    export LD_LIBRARY_PATH="/usr/lib/lapack:/usr/lib/libblas:$LD_LIBRARY_PATH"
    export PYTHONPATH="/cyclus/build:$PYTHONPATH"
    cd $PBS_O_WORKDIR
    aprun -n 1 -N 1 -d 1 -b -- /usr/local/bin/rickshaw -i %(spec_file)s -n %(n)s
    mv *.json %(in_dir)s
    start_time=`date +%%s`
    aprun -n %(n)s -N %(N)s -d 1 -b -- cyclus_script.sh
    end_time=`date +%%s`
    echo Execution time: `expr $end_time - $start_time` s > time.txt
    """

def render_cyclus_script(out_type="sqlite", in_dir=".", out_dir=".",
        log_dir="."):
    rendered_cyclus_script = dedent(CYCLUS_SCRIPT) % {
            "in_dir" : in_dir, "out_dir" : out_dir, "out_type" : out_type,
            "log_dir" : log_dir}

    return rendered_cyclus_script.strip()

def render_pbs_script(nodes, ppn, walltime, spec_file, in_dir):
    rendered_pbs_script = dedent(PBS_SCRIPT) % {"nodes" : str(nodes),
            "ppn" : str(ppn), "walltime" : walltime, "n" : str(nodes*ppn),
            "N" : str(ppn), "spec_file" : spec_file, "in_dir" : in_dir}

    return rendered_pbs_script.strip()

def write_to_files(cyclus_script, pbs_script):
    with open("cyclus_script.sh", "w+") as f:
        f.write(cyclus_script)
    call("chmod +x cyclus_script.sh", shell=True)

    with open("pbs_script.pbs", "w+") as f:
        f.write(pbs_script)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--nodes', dest='nodes', type=int,
            help='Number of nodes', default=1)
    parser.add_argument('--ppn', dest='ppn', type=int,
            help='Number of processors per node', default=1)
    parser.add_argument('--walltime', dest="walltime", type=str,
            help='Wall time', default='00:10:00')
    parser.add_argument('-o', dest='out_type', type=str,
            help='Output type', choices=['sqlite', 'h5'],
            default='sqlite')
    parser.add_argument('--in-dir', dest="in_dir", type=str,
            help='Inputs directory', default='.')
    parser.add_argument('--out-dir', dest="out_dir", type=str,
            help='Outputs directory', default='.')
    parser.add_argument('--log-dir', dest="log_dir", type=str,
            help='Logs directory', default='.')
    parser.add_argument('--spec-file', dest="spec_file", type=str,
            help='Specification file', default='')

    args = parser.parse_args()

    cyclus_script = render_cyclus_script(out_type=args.out_type,
            in_dir=args.in_dir, out_dir=args.out_dir, log_dir=args.log_dir)

    pbs_script = render_pbs_script(args.nodes, args.ppn, args.walltime,
            args.spec_file, args.in_dir)

    write_to_files(cyclus_script, pbs_script)

