# r-roughness-recoding

This repository contains the data and `R` code needed for the replication and extension of the association between "r" and "roughness" reported in Winter, B., Sóskuthy, M., Perlman, M., & Dingemanse, M. (2022). Trilled /r/ is associated with roughness, linking sound and touch across spoken languages. *Scientific Reports*, **12**(1), 1035. [doi:10.1038/s41598-021-04311-7](https://doi.org/10.1038/s41598-021-04311-7), using a new coding of the data.

The structure of the repository is as follows:

+ LICENSE: the GPLv3 license governing our code and data
+ README.md: this README file
+ bibliography.bib: the used references in bib format
+ apa-6th-edition.csl: the APA style used for references
+ IE_recoding_adapted.Rmd and IE_recoding_adapted.html: the Rmarkdown script (and its output) detailing the recoding decisions for each language (please note that this document used mixed English and French languages, but should be understandable even to monolingual English speakers)
+ rrrugosity_revisited.Rmd and rrrugosity_revisited.html: the Rmarkdown script (and its output) containing the analyses reported in the paper
+ data: folder containing various data needed by the rrrugosity_revisited.Rmd script 
  + glottolog: contanins some data downloaded from the Glottolog website
  + phylogenies: contains the two "world" phylogenies from Jäger (2018) and from Bouckaert et al. (2022)
  + rough_r_data_IE.csv, rough_r_data_IE_length.csv and rough_r_data.csv: the recoded data with and without IE languages and with and without form length
+ ComputeFormLength: Python script for the computation of the (rough) form length
+ from_winter2022: various pieces of data and code from the original Winter et al. (2022) paper
+ cached, figures and models: various pre-computed models and figures to speed-up the Rmarkdon compilation process (they can be regenerated if needed using the code in the script but this is quite computationally expensive)
  
 
