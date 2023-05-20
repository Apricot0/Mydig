## Usage

The program is based on the python 3.10 environment. Use python 3.10 interpreter interpret script `mydig.py`. Then the code prompts the user to enter a domain name in the terminal. A dig-like info will be printed to the terminal.  Usage ex:

```bash
(.venv) jasper@ubuntu:~/$ /home/ubuntu/myfile/.venv/bin/python /home/ubuntu/myfile/mydig.py
Enter a domain name: google.co.jp
QUESTION SECTION:
google.co.jp                    IN      A

ANSWER SECTION:
google.co.jp    300     IN      A       142.250.31.94

Query time: 192.782 msec
WHEN: Mon Feb 20 04:52:20 2023
```

## Description

The code defines two functions: `mydig` and `dig` that perform a DNS query to obtain the IP addresses associated with a domain name. The code uses the `dns` library to perform the query, which provides a Python interface to the DNS protocol.

The `mydig` function iteratively queries a list of root DNS servers until it obtains a response or a timeout occurs. The function then checks the additional records in the response for any A records and passes them to the `dig` function to be processed. If no A records are found, the function checks the authority records in the response for any NS records and performs a recursive call to `mydig` with the target domain name. The function also collects any CNAME records that it encounters in the `cname` list.

The `dig` function takes a domain name and a source IP address as input and performs a DNS query using the `dns` library. The function checks the answer section of the response for any A records, collects the IP addresses in the `answers` list, and also checks for any CNAME records and passes them to the `mydig` function to be resolved recursively. If no A or CNAME records are found in the answer section, the function checks the additional records in the response for any A records and passes them to a recursive call to `dig` function. If no additional records are found, the function checks the authority section for any NS records and calls `mydig` with the target domain name.

Finally, the code prompts the user to enter a domain name and measures the time taken to perform the query using the `datetime` library. The result of the query is printed to the console in the format of a standard dig command.

## External Libraries Used

```
dnspython
```

## Some Other Notes

### Plot Folder
The root directory contains a Plot folder, and the graph.py in this folder is used to generate the box plot used in the analysis. When the terminal is in this directory, execute graph.py with the python interpreter. After execution, the user will be promoted to enter the data path. Input data.csv to get box plot of 3 sites, input data2.csv to get box plot of 2 sites. Required external libraries for graph.py:
```
pandas
seaborn
matplotlib
```
Usage ex:
```bash
(.venv) jasper@ubuntu:~/myfile/Plot$ /home/ubuntu/myfile/.venv/bin/python /home/ubuntu/myfile/Plot/graph.py
Enter data input: data.csv
```

### Analyze DNS.pdf
This file is the analysis for the second part of the assignment. It includes procedure, data, box plots and conclusion.

### mydig_output
An output file called “mydig_output”, that contains the expected output for running the mydig program.
