# A script that will take as input a text ast (on the command line) and
# write out a zip file.
import logging
import os
import sys
from servicex.code_generator_service.ast_translator import AstTranslator


def initialize_logging(request=None):
    """
    Get a logger and initialize it so that it outputs the correct format

    :param request: Request id to insert into log messages
    :return: logger with correct formatting that outputs to console
    """

    log = logging.getLogger()
    instance = os.environ.get('INSTANCE_NAME', 'Unknown')
    formatter = logging.Formatter('%(levelname)s ' +
                                  "{} code_generator_funcadl_xaod {} ".format(instance, request) +
                                  '%(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
    log.addHandler(handler)
    log.setLevel(logging.INFO)
    return log


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--ast",
                        help="The text AST to be converted into zip file. STDIN if this is left off")  # noqa: E501
    parser.add_argument("-z", "--zipfile",
                        help="The name of the zip file to write out. STDOUT if this is left off")

    args = parser.parse_args()
    logger = initialize_logging()
    # Get the input AST
    ast_text = args.ast if args.ast is not None else sys.stdin.read().strip()

    # Output file
    translator = AstTranslator()
    zip_data = translator.translate_text_ast_to_zip(ast_text)
    if args.zipfile is None:
        sys.stdout.buffer.write(zip_data)
    else:
        with open(args.zipfile, 'wb') as w:
            w.write(zip_data)
