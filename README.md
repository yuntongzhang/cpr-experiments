# CPR Experiments

Contains setup and results from running [CPR](https://github.com/rshariffdeen/CPR) on the
[VulnLoc](https://github.com/VulnLoc/VulnLoc) benchmark.


## Vulnerabilities

Vulnerability details are in the file `meta-data`.


## Setup details

For each vulnerability, its directory contains files for setting up. Typically, a vulnerability
directory contains the following:

- `setup.sh`: script to download, build, and prepare the program to be run with CPR.
- `components`: components used in patch synthesis.
- `repair.conf`: configuration file for CPR. Specifies the exact components to use and other parameters.
- `spec.smt2`: the specification required for CPR.
- `t1.smt2`: the output smt formula from execution.

In all of the experiments, exactly 5 variables and the operators necessary to fix the bug are supplied
as repair components for patch synthesis. These 5 variables include those used in the developer
patch, plus some others that are irrelevant to the patch.



## Results

The results are the directory `result`. Here, each directory is named with a bug id. In each bug
id directory, the results from running CPR should be interpreted as follows:

- The `<bug id>` subdirectory contains input generated and the ranked patches produced by CPR.
- The file `<bug id>/patch-set-ranked` is the final list of ranked patch produced by CPR.
    - The names appeared in this file and the component names, instead of the real names in the program.
    To map it back to program variable names, refer to the `setup.sh` file in the setup directory
    and find the line with `__trident_choice`.
    - From the top-ranked patch, the patch list is checked one by one until a patch that is the same
    as the developer patch is found. The rank of this patch is the final ranked reported.
- The file `log-latest` contains the log from CPR.
    - If a CPR run is successful (i.e. not timeout), the last part of this log file contains two lines
    with `Patch Start Count` (`sc`) and `Patch End Count` (`ec`), showing the initial patch number
    from synthesis and the final patch number after concolic execution.
    - The reported patch pool reduction ratio is calculated as `1 - ec/sc`.



## Steps used in experiments

To run CPR on the experiment benchmark, the following steps were performed:

1. Run pre-built docker container:

```bash
docker pull rshariffdeen/cpr:experiments-cpr
docker run --name cpr-container -it rshariffdeen/cpr:experiments-cpr bash
```

2. Inside the container, clone this repository:

```bash
cd /
git clone https://github.com/yuntongzhang/cpr-experiments.git
cd cpr-experiments
```

3. Run the driver script to run CPR on the vulnerabilties:

```
python3.7 driver.py
```

To run individual vulnerability, do:

```
python3.7 driver.py --bug-id=X
```
where `X` is the `id` field from `meta-data` file.
