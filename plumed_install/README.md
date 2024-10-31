# PLUMED Installation Guide

PLUMED is a powerful open-source library for free energy calculations and enhanced sampling in molecular dynamics simulations. This guide will walk you through the steps to install PLUMED 2.9.2 on your system. See also https://www.plumed.org/doc-v2.9/user-doc/html/index.html 

## Prerequisites

- C and C++ compilers (e.g., GCC, Clang)
- CMake (version 3.10 or newer)
- MPI library (optional, for parallel processing)
- LAPACK and BLAS libraries (optional, for some PLUMED features)

## Installation Steps

1. **Download PLUMED**:
   - Visit the PLUMED download page: https://www.plumed.org/download
   - Choose the PLUMED 2.9.2 version for your system
   - Download the source code package (e.g., `plumed-2.9.2.tgz`)

2. **Extract the source code**:
   ```bash
   tar -xzf plumed-2.9.2.tgz
   cd plumed-2.9.2
   ```

3. **Configure the build**:
   ```bash
   ./configure \
     --prefix=/path/to/install \
     --enable-mpi \
     --enable-shared \
     --enable-modules="all" \
     --with-fftw3 \
     --with-lapack \
     --with-blas
   ```
   - `--prefix=/path/to/install`: Specifies the installation directory for PLUMED
   - `--enable-mpi`: Enables building PLUMED with MPI support for parallel processing
   - `--enable-shared`: Enables building shared libraries
   - `--enable-modules="all"`: Enables building all available PLUMED modules
   - `--with-fftw3`: Enables support for the FFTW3 library
   - `--with-lapack`: Enables support for the LAPACK library
   - `--with-blas`: Enables support for the BLAS library

   If you need more information about the available configuration options, you can run:

   ```
   ./configure --help
   ```

4. **Build PLUMED**:
   ```bash
   make -j4
   ```
   The `-j4` option uses 4 parallel jobs to speed up the build process. Adjust the number based on the available CPU cores on your system.

5. **Install PLUMED**:
   ```bash
   make install
   ```

6. **Set the environment properly**:
   One should then set the environment properly. We suggest to do it using the module framework (http://modules.sourceforge.net). An ad hoc generated module file for PLUMED can be found in `$prefix/lib/plumed/src/lib/modulefile`. Just edit it as you wish and put it in your modulefile directory. This will also allow you to install multiple PLUMED versions on your machine and to switch among them. If you do not want to use modules, you can still have a look at the modulefile we did so as to know which environment variables should be set for PLUMED to work correctly.

## Patching your MD code

A growing number of MD codes can use PLUMED without any modification. If you are using one of these codes, refer to its manual to know how to activate PLUMED. In case your MD code is not supporting PLUMED already, you should modify it. We provide scripts to adjust some of the most popular MD codes so as to provide PLUMED support. At the present times we support patching the following list of codes:

- gromacs-2020-7
- gromacs-2021-7
- gromacs-2022-5
- gromacs-2023-5
- gromacs-2024-3
- namd-2-12
- namd-2-13
- namd-2-14
- qespresso-5-0-2
- qespresso-6-2
- qespresso-7-0
- qespresso-7-2

In the section "Code specific notes" you can find information specific for each MD code.

To patch your MD code, you should have already installed PLUMED properly. This is necessary as you need to have the command "plumed" in your execution path. As described above, this executable will be in your paths if PLUMED was installed or if you have run `sourceme.sh`.

Once you have a compiled and working version of PLUMED, follow these steps to add it to an MD code:

1. Configure and compile your MD engine (look for the instructions in its documentation).
2. Test if the MD code is working properly.
3. Go to the root directory for the source code of the MD engine.
4. Patch with PLUMED using:
   ```
   plumed patch -p
   ```
   The script will interactively ask which MD engine you are patching.
5. Once you have patched, recompile the MD code (if dependencies are set up properly in the MD engine, only modified files will be recompiled).

## Troubleshooting

If you encounter any issues during the installation or patching, check the PLUMED documentation or seek help from the PLUMED community forums.