# Control over Wireless Analysis Scripts

Traces are stored in `/tools/cow/`.

The `summarize.py` script takes two arguments:
*) The path to an input `dat` file, a binary file containing real/imag pairs (each is a short).
*) The path to an output file to append summary stastistics to

To run the summarize script on every `dat` file in a directory, you can use find:
```
find /tools/cow/path/to/directory -type f -exec ./summarize.py {} output_file_name.txt \; &
```

The `visualize.py` script takes one input:
1) The output file from the summarize script

and then a number of other inputs to select which plots to generate.


