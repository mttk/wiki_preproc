import os, sys
import re
import ftfy
import spacy
import argparse

from tqdm import tqdm

"""
Step 1. Download an english dump of Wikipedia from: https://dumps.wikimedia.org/enwiki/
        The file you are looking for is labeled "[en]wiki-[identifier]-pages-articles.xml.bz2"
        ## https://en.wikipedia.org/wiki/Wikipedia:Database_download#English-language_Wikipedia
Step 2. Run wikiextractor on the downloaded corpus
        The output document format is explained here:
        http://medialab.di.unipi.it/wiki/Document_Format
Step 3. Convert the wikiextracted format to plaintext and run ftfy
Step 4. Run sentence tokenization w/ SpaCy
"""

def make_parser():
  parser = argparse.ArgumentParser(description='Wikipedia preprocessing toolkit')
  parser.add_argument('--input', type=str, help='Wikipedia corpus preprocesed with wikiextractor', required=True)
  parser.add_argument('--data_out', type=str, help='File to store tokenized data in', required=True)
  parser.add_argument('--header_out', type=str, help='Output file with document headers', default="")  
  return parser

def load_wikiextractor_format(path_to_file):
  DOCSTART = '<doc'
  DOCEND = '</doc'

  in_doc = False
  cur_doc_lines = []

  with open(path_to_file, 'r') as infile:
    for idx, line in tqdm(enumerate(infile)):
      if line.startswith(DOCSTART):
        assert not in_doc, f"Beginning of new document within an existing document, line #{idx}!"
        line = line.strip()[1:-1] # remove "<", ">"
        # first element of the first split is the "doc" identifier
        # we use split "=", 1 not to split by equals signs within the descriptors
        parts = [tuple(part.split("=", 1)) for part in line.split()[1:]]
        # strip quotes from values
        header = {k:v.strip('"') for k,v in parts}
        in_doc = True
      elif line.startswith(DOCEND):
        assert in_doc, f"Document ended when no document was open, line #{idx}!"
        in_doc = False
        yield header, cur_doc_lines
        cur_doc_lines = []
      else:
        line = line.strip()
        if not line: continue
        cur_doc_lines.append(line)

def spacy_for_sentence_splitting(language='en'):
  nlp = spacy.load(language, disable=['ner', 'tagger', 'parser'])
  nlp.add_pipe(nlp.create_pipe('sentencizer'))
  return nlp

def sentencize_article(article_lines, nlp):
  sentences = []
  for paragraph in nlp.pipe(article_lines):
    for sent in paragraph.sents:
      sentences.append(str(sent))
  return sentences

def apply_sentence_hooks(sentences, hooks):
  cleaned_sentences = []
  for sentence in sentences:
    for hook in hooks:
      sentence = hook(sentence)
    if sentence: cleaned_sentences.append(sentence)
  return cleaned_sentences

HTML_TAG_REGEX = re.compile('<.*?>')
def clean_html(raw_html):
  cleantext = re.sub(HTML_TAG_REGEX, '', raw_html)
  return cleantext

def main():
  args = make_parser().parse_args()
  spacy = spacy_for_sentence_splitting()

  sentence_level_hooks = [ftfy.fix_text, clean_html]

  with open(args.data_out, 'w') as data_out, open(args.header_out, 'w') as header_out:
    for header, doc_lines in load_wikiextractor_format(args.input):
      header_string = '\t'.join([f"{key}:{value}" for key, value in header.items()])
      header_out.write(header_string + "\n")

      # Apply ftfy, then sentencize
      sentencized_doc = sentencize_article(doc_lines, spacy)

      if sentence_level_hooks:
        sentencized_doc = apply_sentence_hooks(sentencized_doc, sentence_level_hooks)

      data_out.write("\n".join(sentencized_doc)+"\n\n") # newline delimits documents

if __name__ == '__main__':
  main()
