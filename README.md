# Identic
A Python program which is used to find duplicate(i.e identical) files and directories in the system with the purpose of emptying space.

## Running Program
``` bash
python identic.py [-f | -d] [-i] [-c] [-n] [-s] [<dir1> <dir2> ...]
```

-f | -d => -f means look for identical files, -d means look for identical directories. The default is identical files 


-c => Identical will mean the contents are exactly the same(note that the names can be different). 


-n => Identical will mean the directory/file names are exactly the same(not that the contents can be different.


-cn => Identical will mean both the contents and the directory/file names are exactly the same.


[< dir1 > < dir2 > ..] => The list of directories to traverse. The default is current directory.
  
  
-s  => The size for each duplicate will be printed. This option is ignored when -n option is used.
  
  
