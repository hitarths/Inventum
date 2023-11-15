# Inventum
Inventum: Discovering Favorites in Databases via Interactive Regret Minimization


Run the command:

1. Setup a Python environment with 
    ```python3 -mvevn inventum-env```
    And activate with 
    ```source inventum-env/bin/activate```
2. Install all the required libraries:
    ```pip install -r requirement.txt```
3. Run the following command to get help running Inventum:

    ```python3 main.py
    usage: main.py [-h] --database DATABASE [--criterion {LP,bruteforce}] [--looseness LOOSENESS] [--negative-attributes NEGATIVE_ATTRIBUTES]
               [--utility-function UTILITY_FUNCTION]
    main.py: error: the following arguments are required: --database
    ```
4. Example command:
    ```Inventum % python3 main.py --database players --criterion LP --looseness 0 --utility-function '[-1]' --negative-attributes '[0]' --cutoff 1000```