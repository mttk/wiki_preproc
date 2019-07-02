#!/bin/sh
# Run this script from the root directory of the package

# Please set absolute paths
PATH_TO_WIKI=/your/path/here
WIKI_OUTPUT_DIR=/your/path/here
WIKI_OUTPUT_FILE=preprocessed_wiki.txt
WIKI_HEADER_FILE=wiki_header.txt
MAX_OUTPUT_SIZE=20G
MIN_TEXT_LENGTH=50

# 1. Run wikiextractor
cd wikiextractor

echo "Running wikiextractor ... this will take some time"
python WikiExtractor.py $PATH_TO_WIKI --bytes $MAX_OUTPUT_SIZE --filter_disambig_pages --min_text_length $MIN_TEXT_LENGTH -o $WIKI_OUTPUT_DIR

# Here we assume that you will set MAX_OUTPUT_SIZE large enough
# so that the whole wikipedia will be stored in one file.
# Otherwise: the outputs will be stored in folders starting
# from "AA -- ZZ", containing files named "wiki_00" -- "wiki_99"

# 2. Preprocess wikipedia (sentencize, clean, strip wikiextractor output format)
echo "Running wikipedia preprocessing ... this will take some time"
cd ..
PROCESSED_WIKI=$WIKI_OUTPUT_DIR/AA/wiki_00
python process_wiki.py --input $PROCESSED_WIKI --data_out $WIKI_OUTPUT_DIR/$WIKI_OUTPUT_FILE --header_out $WIKI_OUTPUT_DIR/$WIKI_HEADER_FILE
