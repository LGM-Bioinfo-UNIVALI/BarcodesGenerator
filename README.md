# BarcodesFilter
 Filter barcodes based on some criteria



---
### :warning: Requirements:
- Generate Barcodes:
    To Generate barcodes via BarcodesFilter you have to:
    - <img src="https://github.com/devicons/devicon/blob/master/icons/linux/linux-original.svg" title="Linux" alt="Linux" width="20" height="20"/>&nbsp; <img src="https://github.com/devicons/devicon/blob/master/icons/bash/bash-original.svg" title="Bash" alt="Bash" width="20" height="20"/>&nbsp; Use a machine with a **linux** distribution that uses **bash** as shell
    - Install rsat package via conda environment: you can check the installation tutorial [here](https://rsa-tools.github.io/installing-RSAT/conda-install-rsat/bioconda-rsat-core.html "RSAT Installation Tutorial")  
        </br>
        OBS: Errors can occur because of conflits with the python version. You can fix that by installing rsat via mamba instead of conda, like this:  
        &nbsp; &nbsp; Install mamba
        ```shell
        conda install -n base conda-forge::mamba
        ```
        &nbsp; &nbsp; Create 'rsat' conda environment with python 3.7
        ```shell
        mamba create -n rsat python=3.7
        ```
        &nbsp; &nbsp; Activate environment
        ```shell
        conda activate rsat
        ```
        &nbsp; &nbsp; Install rsat
        ```shell
        mamba install -c bioconda rsat-core
        ```

- General:
    - <img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original.svg" title="Python" alt="Python" width="20" height="20"/>&nbsp; Python 3.7
    - <img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original.svg" title="Python" alt="Python" width="20" height="20"/>&nbsp; Python Libraries/Modules:
        - YAML
        - Biopython
        - Difflib

---
### :broom: Barcodes Filter Criteria

- Filter by Baseruns:

> Discard sequences with baseruns (base repetition) bigger than the max number defined by the user
> &nbsp; &nbsp;Example:
> &nbsp; &nbsp; &nbsp; Max baserun = 2
> &nbsp; &nbsp; &nbsp; Sequence: ACAATG -> will not be discarded
> &nbsp; &nbsp; &nbsp; Sequence: ACAAATG -> will be discarded because of 'AAA'

- Filter by Common Subsequence between barcodes:

> Discard barcodes that contain same subsequence (with min size defined by the user) as an already selected barcode

---
### :memo: Tutorial

- User configuration is defined via the **config.yaml** file, like this:

explicar que os barcodes podem vir num arquivo txt (um abaixo do outro) ou fasta (com identificadores)

---