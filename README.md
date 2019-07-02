## Wikipedia preprocessing tool

### Installation and running instructions

1. Clone the repository and its submodules `git clone --recurse-submodules -j8 git@github.com:mttk/wiki_preproc.git`
2. Install the requirements `pip install -r requirements.txt`
3. Download he spacy model for the language you want `python -m spacy download en`
4. Download and store the wikipedia dump (from https://dumps.wikimedia.org/enwiki/ for English dumps) 
  - ex. `wget https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2` for the latest dump of english wiki
5. Modify the paths and parameters in `clean_wiki.sh` and run the script `./clean_wiki.sh`

### Description

The output provided by this tool is a sentence-level tokenized dump of wikipedia. Wikipedia articles are separated by empty lines, and each line is a separate sentence. The output format is in line with BERT input and can be used with repositories such as pytorch-pretrained-BERT.