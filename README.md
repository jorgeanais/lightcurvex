# lightcurvex
Tools used to extract light curves from VVVX data


##  Instructions for getting the data from the repository

query
```
search: 198.B-2004
additional sql: obj like '%411'
```

Notice that the database schema (column names) can be accessed here: http://casu.ast.cam.ac.uk/vistasp/imgquery/schema

Instruction to download the fits tables
```bash
wget --http-user=username --http-passwd=password \
        http://casu.ast.cam.ac.uk/~eglez/vistasp/requests/XXXXXXXXXXX/filelist
wget --http-user=username --http-passwd=password \
       -m -B http://casu.ast.cam.ac.uk/~eglez/vistasp/requests/XXXXXXXXXXX/ -i filelist
```

## Instructions for converting the fits tables to ascii

Use the provided fortan code to convert the fits tables to ascii. The code is in the `assests/` folder. The code is compiled with `gfortran` and the command to compile it is:

```bash
gfortran fitsio_cat_list.f -o fitsio_cat_list -L/sw/lib -lcfitsio -lm
```
It requires the `cfitsio` library to be installed. To install it in ubuntu I used `sudo apt install libcfitsio-bin libcfitsio-dev libcfitsio-doc libcfitsio9`.

The script convert_tables.sh can be used to convert all the tables in the current folder. It requires the `fitsio_cat_list` executable to be in the same folder.

I put the executable in my $HOME/bin folder and added that folder to my $PATH variable. I also added the following line to my .bashrc file:

```bash
export PATH=$HOME/bin:$PATH
```

The columns of the output file are:
RA and Dec coordiantes, x, y, magnitude, magnitude error, chip number, stellar classification, ellipticity and position angle.