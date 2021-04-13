# # download link: https://www.tbi.univie.ac.at/RNA/documentation.html#install

# wget https://www.tbi.univie.ac.at/RNA/download/sourcecode/2_4_x/ViennaRNA-2.4.17.tar.gz
# tar -zxvf ViennaRNA-2.4.17.tar.gz
# cd ViennaRNA-2.4.17
# ./configure --enable-universal-binary #use this for MacOSX
# # ./configure 
# # checking if malloc debugging is wanted... no
# # checking for gcc... gcc
# # checking whether the C compiler works... no
# # configure: error: in `/Users/albert/Dropbox/Floor Lab/Analysis/UTR_library/ViennaRNA-2.4.17/src/Kinfold':
# # configure: error: C compiler cannot create executables
# # See `config.log' for more details
# # configure: error: ./configure failed for src/Kinfold


# make

# #   CXXLD    libRNA_conv.la
# # ../../libtool: line 1856: cd: /Users/albert/Dropbox/Floor: No such file or directory
# # make[4]: *** [libRNA_conv.la] Error 1
# # make[3]: *** [all-recursive] Error 1
# # make[2]: *** [all-recursive] Error 1
# # make[1]: *** [all-recursive] Error 1
# # make: *** [all] Error 2

tar -zxvf ViennaRNA-2.4.17.tar.gz   
cd ViennaRNA-2.4.17
./configure --prefix=/home/albert/ViennaRNA   
make      
sudo make install    