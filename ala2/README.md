# Ala2 Peptide Simulation with GROMACS

This guide will walk you through the steps to simulate the Ala2 (alanine dipeptide) molecule using the GROMACS molecular dynamics software.

## Notes

- The `./mdp/` directory should contain the GROMACS parameter files (`.mdp`) for energy minimization, NVT equilibration, and production MD simulation.
- Ensure that the `ala2.pdb` file is available in the working directory.
- The `gmx_mpi` commands assume that you have built GROMACS with MPI support. If you don't have MPI, you can use the regular `gmx` commands instead.

## Simulation Steps

1. **Prepare the input structure**:
   ```bash
   gmx_mpi pdb2gmx -f ala2.pdb
   ```
   This command converts the PDB file `ala2.pdb` into a GROMACS-compatible topology and coordinate files.

2. **Create a simulation box**:
   ```bash
   gmx_mpi editconf -f conf.gro -o box.gro -bt cubic -d 1.0
   ```
   This command creates a cubic simulation box with a 1.0 nm distance from the solute to the box edges.

3. **Solvate the system**:
   ```bash
   gmx_mpi solvate -cp box.gro -o sol.gro -p topol.top
   ```
   This command adds water molecules to the simulation box and updates the topology file `topol.top`.

4. **Energy minimization**:
   ```bash
   gmx_mpi grompp -o em.tpr -f ./mdp/em.mdp -c sol.gro
   gmx_mpi mdrun -s em.tpr -c em.gro -e em.edr
   ```
   These commands perform energy minimization on the solvated system using the parameters defined in the `em.mdp` file.

5. **NVT equilibration**:
   ```bash
   gmx_mpi grompp -o nvt.tpr -f ./mdp/nvt.mdp -c em.gro -r em.gro
   gmx_mpi mdrun -s nvt.tpr -c nvt.gro
   ```
   These commands perform NVT (constant Number, Volume, and Temperature) equilibration using the parameters defined in the `nvt.mdp` file.

6. **Production MD simulation**:
   ```bash
   gmx_mpi grompp -o md.tpr -f ./mdp/md.mdp -c nvt.gro
   gmx_mpi mdrun -s md.tpr -c md.gro -o md.trr -x md.xtc -v
   ```
   These commands run the production molecular dynamics simulation using the parameters defined in the `md.mdp` file. The simulation trajectory is saved in the `md.trr` and `md.xtc` files, and the final coordinates are written to `md.gro`.

7. **Analysis trajectory with plumed**:
   ```bash
   plumed driver --mf_trr md.trr --plumed plumed.dat
   ```
   This command calculates describtors of points in trajectory `md.trr`.

7. **Production MD simulation with Metadynamics**:
   ```bash
   gmx_mpi mdrun -s md.tpr -c md.gro -o md.trr -x md.xtc -plumed_metad.dat -v
   ```
   This command runs the production molecular dynamics simulation with metadynamics.



## Troubleshooting

If you encounter any issues during the simulation, refer to the GROMACS documentation or seek help from the GROMACS community forums.