# tests with BPE tokenizer
#
# sample usage:
#
#   python3 tests/test-tokenizer-0-bpe.py ~/Data/huggingface/Meta-Llama-3-8B-Instruct/
#   python3 tests/test-tokenizer-0-bpe.py ~/Data/huggingface/falcon-7b/
#   python3 tests/test-tokenizer-0-bpe.py ~/Data/huggingface/deepseek-coder-6.7b-instruct/
#

import logging
import argparse

from transformers import AutoTokenizer

logger = logging.getLogger("test-tokenizer-0-bpe")

parser = argparse.ArgumentParser()
parser.add_argument("dir_tokenizer", help="directory containing 'tokenizer.model' file")
parser.add_argument("--fname-tok",   help="path to a text file to tokenize")
parser.add_argument("--verbose", action="store_true", help="increase output verbosity")

args = parser.parse_args()
logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
dir_tokenizer = args.dir_tokenizer

tokenizer = AutoTokenizer.from_pretrained(dir_tokenizer)

tests = [
    "",
    " ",
    "  ",
    "   ",
    "\t",
    "\n",
    "\n\n",
    "\n\n\n",
    "\t\n",
    "Hello world",
    " Hello world",
    "Hello World",
    " Hello World",
    " Hello World!",
    "Hello, world!",
    " Hello, world!",
    " this is 🦙.cpp",
    "w048 7tuijk dsdfhu",
    "нещо на Български",
    "កាន់តែពិសេសអាចខលចេញ",
    "🚀 (normal) 😶‍🌫️ (multiple emojis concatenated) ✅ (only emoji that has its own token)",
    "Hello",
    " Hello",
    "  Hello",
    "   Hello",
    "    Hello",
    "    Hello\n    Hello",
    " (",
    "\n =",
    "' era",
    "Hello, y'all! How are you 😁 ?我想在apple工作1314151天～",
    "3",
    "33",
    "333",
    "3333",
    "33333",
    "333333",
    "3333333",
    "33333333",
    "333333333",
]

for text in tests:
    logger.info(f"text: {text}")
    logger.info(tokenizer.encode(text))
    logger.info(tokenizer.decode(tokenizer.encode(text)))

logger.info("tests for C++:")
for text in tests:
    res = tokenizer.encode(text)

    # Modify text representation for logging
    k = text.replace('\n', '\\n')
    k = k.replace('\t', '\\t')
    k = '"' + k + '"'

    # Log the modified text and its encoding
    log_message = "{ %-24s, { " % k
    for x in res:
        log_message += "%7d," % x
    log_message += " }, },"
    logger.info(log_message)

logger.info(tokenizer.encode('hello'))
logger.info(tokenizer.encode('world'))
logger.info(tokenizer.encode(' world'))
logger.info(tokenizer.encode('hello world'))

fname_tok = args.fname_tok
if fname_tok:
    logger.info(f"tokenizing file: {fname_tok}")
    fname_out = fname_tok + '.tok'
    with open(fname_tok, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        s = ''.join(lines)
        res = tokenizer.encode(s)
        # write to file
        with open(fname_out, 'w', encoding='utf-8') as f:
            for x in res:
                # LLaMA v3 for some reason strips the space for these tokens (and others)
                # if x == 662:
                #     f.write(str(x) + ' \' ' + tokenizer.decode(x) + '\'\n')
                # elif x == 1174:
                #     f.write(str(x) + ' \' ' + tokenizer.decode(x) + '\'\n')
                # elif x == 2564:
                #     f.write(str(x) + ' \' ' + tokenizer.decode(x) + '\'\n')
                # elif x == 758:
                #     f.write(str(x) + ' \' ' + tokenizer.decode(x) + '\'\n')
                # elif x == 949:
                #     f.write(str(x) + ' \' ' + tokenizer.decode(x) + '\'\n')
                # elif x == 5354:
                #     f.write(str(x) + ' \' ' + tokenizer.decode(x) + '\'\n')
                # else:
                #     f.write(str(x) + ' \'' + tokenizer.decode(x) + '\'\n')
                f.write(str(x) + ' \'' + tokenizer.decode(x).strip() + '\'\n')
        logger.info(f"len(res): {len(res)}")
        logger.info(f"len(lines): {len(lines)}")
    logger.info(f"results written to: {fname_out}")
