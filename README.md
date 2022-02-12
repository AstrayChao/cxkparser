# cxkparser

For genome Sequencing / Annotation

website: https://marinegenomics.oist.jp/habu/

# Install

```
1. git clone https://github.com/AstrayChao/cxkparser.git
2. cd cxkparser
3. python setup install
```

# Usage
```
usage: cxkParser [-h] --path PATH --output OUTPUT [--thread_nums THREAD_NUMS]

optional arguments:
  -h, --help            show this help message and exit
  --path PATH, -p PATH  Please input the path where the file is located
  --output OUTPUT, -o OUTPUT
                        Please input the output directory and file name of the file. e.g. /home/cxkparser/file_name.
                        If you do not input the file name, the default file name is annotation_<original file name>. e.g. /home/cxkparser/annotation_file_name.xlsx
  --thread_nums THREAD_NUMS, -n THREAD_NUMS
                        Please input the number of threads, Multi-threading is not enabled by default
```
