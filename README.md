## Setting Up the Project
### Prerequesites
- Install and Open Miniconda / Anaconda Prompt. (Available on Silva)

- Optional: Install Git for Windows to easily pull the most recent version of the program.

### **Install dependencies**

   If you configured your .condarc with your api token correctly and have been added to an openpaas subscription, you can install the project dependencies using conda:

   ```sh
   conda install pandas
   ```
   ```sh
   conda install openpyxl
   ```
Once these are set up, your batch scripts can be used to run the python program.

### **How to Run the Script**
1. Double-click on transform_files.bat to run the script
2. Write "all" if you want to tranform all files. Alternatively, use the file names defined in the config separated with comma to transform specific files.
