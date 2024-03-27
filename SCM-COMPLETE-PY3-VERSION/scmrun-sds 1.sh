#!/bin/bash
#SBATCH --ntasks-per-node 24
#SBATCH --error=job.%J.err
#SBATCH --output=job.%J.out
#SBATCH -p all.q

INP_FILES=""

OUT_FILES=""

JOB_DIR="$SLURM_JOBID"_$SLURM_JOB_NAME
SCRATCH_DIR=/apps/scratch/rdg/darpanks/$JOB_DIR
mkdir $SCRATCH_DIR

mpirun -n 1  python2  __main__.py "Failure-rate-model-Diagnostic-0p00001pf" "ShutdownSysRod1_DIAGNOSTIC"

