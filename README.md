# BarcodesFilter
 Filter barcodes based on some criteria




### :warning: Dependencies:
---
- Generate Barcodes:
    To Generate barcodes via BarcodesFilter you have to:
    - Use a machine with a linux distribution that uses bash as shell
    - Install 'rsat' package via conda environment
        You can check the installation tutorial here https://rsa-tools.github.io/installing-RSAT/conda-install-rsat/bioconda-rsat-core.html
        OBS: Errors can occur because of conflits with the python version. You can fix that by installing 'rsat' via mamba instead of conda, like this:
        conda install -n base conda-forge::mamba # Install mamba
        mamba create -n rsat python=3.7  # Create 'rsat' conda environment with python 3.7
        conda activate rsat  # Activate environment
        mamba install -c bioconda rsat-core  # Install 'rsat'

- General:
    -python x.x
    -library x

---

filter criteria:
xxxxxx

usage:
xxxxxx
explicar que os barcodes podem vir num arquivo txt (um abaixo do outro) ou fasta (com identificadores)
