# GROMACS Installation Guide

GROMACS (Groningen Machine for Chemical Simulations) is a versatile package for molecular dynamics simulations and analysis. This guide will walk you through the installation process on a Linux or macOS system. See also https://manual.gromacs.org/current/install-guide/index.html


## Installation Steps

1. **Download GROMACS**:
   - Visit the GROMACS download page: https://www.gromacs.org/Downloads
   - Choose the appropriate version for your system (e.g., 2024.3)
   - Download the source code package (e.g., `gromacs-2024.3.tar.gz`)

2. **Extract the source code**:
   ```bash
   tar -xzf gromacs-2024.3.tar.gz
   cd gromacs-2024.3
   ```

3. **Create a build directory**:
   ```bash
   mkdir build
   cd build
   ```

4. **Configure the build**:
   ```bash
   cmake .. -DGMX_BUILD_OWN_FFTW=ON -DREGRESSIONTEST_DOWNLOAD=ON
   ```
   - `-DCMAKE_C_COMPILER=xxx`: Specifies the name of the C99 compiler to use (or the environment variable `CC`)
   - `-DCMAKE_CXX_COMPILER=xxx`: Specifies the name of the C++17 compiler to use (or the environment variable `CXX`)
   - `-DGMX_MPI=on`: Enables building GROMACS with MPI support for parallel processing
   - `-DGMX_GPU=CUDA`: Enables building GROMACS with NVIDIA CUDA support
   - `-DGMX_GPU=OpenCL`: Enables building GROMACS with OpenCL support
   - `-DGMX_GPU=SYCL`: Enables building GROMACS with SYCL support (using Intel oneAPI DPC++ by default)
   - `-DGMX_SYCL=ACPP`: Enables building GROMACS with SYCL support using AdaptiveCpp (hipSYCL), requires `-DGMX_GPU=SYCL`
   - `-DGMX_SIMD=xxx`: Specifies the level of SIMD support for the target system
   - `-DGMX_DOUBLE=on`: Enables building GROMACS in double precision (slower, and not normally useful)
   - `-DCMAKE_PREFIX_PATH=xxx`: Adds a non-standard location for CMake to search for libraries, headers, or programs
   - `-DCMAKE_INSTALL_PREFIX=/path/to/install`: Specifies the installation directory for GROMACS (default is `/usr/local/gromacs`)
   - `-DBUILD_SHARED_LIBS=off`: Turns off the building of shared libraries to help with static linking
   - `-DGMX_FFT_LIBRARY=xxx`: Selects the FFT library to use (fftw3, mkl, or fftpack)
   - `-DCMAKE_BUILD_TYPE=Debug`: Builds GROMACS in debug mode

5. **Build GROMACS**:
   ```bash
   make -j4
   ```
   The `-j4` option uses 4 parallel jobs to speed up the build process. Adjust the number based on the available CPU cores on your system.

6. **Install GROMACS**:
   ```bash
   make install
   ```

7. **Verify the installation**:
   ```bash
   /path/to/install/bin/gmx --version
   ```
   This should display the installed GROMACS version.

8. **Source the GMXRC file**:
   ```bash
   source /usr/local/gromacs/bin/GMXRC
   ```
   This step is necessary to set up the environment variables for GROMACS. Replace `/usr/local/gromacs` with the actual installation prefix if you used a different one.


