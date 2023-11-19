import time

from Parser.Inception import Inception
import logging
import datetime, sys, os
import pandas as pd

def setup_logging(filename):
    logging.basicConfig(
        format='Date-Time : %(asctime)s : Line No. : %(lineno)d - %(message)s',
        level=logging.DEBUG,
        encoding='utf-8',
        filemode='w'
    )

    # Create a log handler to save logs to a file
    ct = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")
    root_dir = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(root_dir, 'logs', f'{filename}_{ct}.log')
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('Date-Time : %(asctime)s : Line No. : %(lineno)d - %(message)s')
    file_handler.setFormatter(formatter)
    logging.getLogger().addHandler(file_handler)

def main(files):

    file_lst = list(filter(None, files.split(";")))
    df_list = []

    for filename in file_lst:
        setup_logging(filename)

        cInception = Inception(filename=filename, linesToSkip=4)

        df = cInception.load_notations()
        if df is None:
            logging.info(">>> Failed to load notations.")
            return

        logging.info(f">>> {len(df)}")

        df = df[df['category_entity'] != '_']
        if df is None:
            logging.info(">>> Failed to filter data.")
            return

        logging.info(f">>> {len(df)}")

        df = cInception.order_entity_words_by_index(df)
        if df is None:
            logging.info(">>> Failed to order entity words by index.")
            return

        logging.info(f">>> {len(df)}")

        df = cInception.concatenate_word_entity(df)
        if df is None:
            logging.info(">>> Failed to concatenate word entities.")
            return

        logging.info(f">>> {len(df)}")

        df = cInception.concatenate_word_and_text(df)
        if df is None:
            logging.info(">>> Failed to concatenate final word entities.")
            return

        logging.info(f">>> {len(df)}")

        df = cInception.add_column_filename(df)
        if df is None:
            logging.info(">>> Failed to add field name column.")
            return

        logging.info(f">>> {len(df)}")

        cInception.write_csv_old(df, cInception.fileName)

        df_list.append(df)
        time.sleep(5)

    logging.info(">>> Aggregated CSV file:")
    df_aggregated = pd.concat(df_list, ignore_index=False)
    cInception.write_csv_old(df_aggregated, "freguesias_aggregated")
    logging.info(">>> Finish!")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        main(filename)
    else:
        print("Por favor, forneça o nome do arquivo como argumento.")