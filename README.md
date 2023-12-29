## Setting Up the Project
This is a simple, config-focused python program to allow the transformation of csv & excel files into the desired output format. It's useful in scenarios where GUI-based solutions like KNIME or ALTERYX are prohibited by company guidelines.

### Prerequesites
- Install and Open Miniconda / Anaconda Prompt.

### **Install dependencies**
Install the project dependencies using conda:

```sh
conda install pandas
```
```sh
conda install openpyxl
```

or simply 

```sh
pip install -r requirements.txt
```

Once these are set up, your batch scripts can be used to run the python program.

### **How to Run the Script**
1. Double-click on transform_files.bat to run the script
2. Write "all" if you want to tranform all files. Alternatively, use the file names defined in the config separated with comma to transform specific files.

### Note
You'll need to edit the path in the batch scripts to use the correct conda distribution.
