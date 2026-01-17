#!/usr/bin/python
import logging, csv, datetime, os
import time

import os
import datetime
import pandas as pd
import logging

class Inception():
    def __init__(self,
                 encodingToWrite = "utf-8-sig",
                 delimiter = "\t",
                 linesToSkip = 5,
                 filename = str):

        self.encodingToWrite = encodingToWrite
        self.delimiter = delimiter
        self.linesToSkip = linesToSkip
        self.fileName = filename

    def load_notations(self):

        """
        Load notations from a TSV file and parse them into a structured format.

        This function reads a TSV (Tab-Separated Values) file containing notations and parses them into a structured format.
        The file is expected to have specific column formats representing different aspects of the notations, such as the
        position, word, entity, and category. The function iterates through the file, extracts the relevant information,
        and creates a pandas DataFrame with the parsed notations.

        Args:
            None
        Returns:
            pd.DataFrame: A DataFrame containing the parsed notations.
        """

        # Get the root directory of the project
        root_dir = os.path.dirname(os.path.abspath(__file__))
        # Build the absolute path to a data file
        file_path = os.path.join(root_dir, '..', 'data/DataToParse', f'{self.fileName}.tsv')

        try:
            text = []
            notations = []
            previous_line_length = 0
            text_quantity = 0

            with open(file_path, encoding='utf-8') as file:
                tsv_file = csv.reader(file, delimiter=self.delimiter)
                for skip_line in range(self.linesToSkip):
                    next(tsv_file)

                for line in tsv_file:
                    line_length = len(line)

                    if line_length == 0:
                        logging.info(f">>> Text annotated: {text}")
                        logging.info(f">>> {len(notations)} - Finished parsing!")
                        text = []
                        text_quantity = text_quantity + 1
                    elif line_length == 1:
                        if previous_line_length > 1:
                            logging.info(f">>> {len(notations)} - Finished parsing!")
                            text = []

                        logging.info(f">>> {len(notations)} - >>> Text annotated {line}")
                        text.append(''.join(str(item) for item in line))
                        #logging.info(type(''.join(str(item) for item in line)))
                    elif line_length >= 6:
                        logging.info(f">>> {len(notations)} - {line} ({line_length})")
                        notation_dict = {
                            'text': ''.join(str(item) for item in text),
                            'qty_phrase': len(''.join(str(item) for item in text)),
                            'pos_word': line[0],
                            'pos_characters_word': line[1],
                            'word': line[2],
                            'entity': line[3],
                            'category_entity': line[4],
                            'undefined1': line[5],
                            'undefined2': line[6] if len(line) > 6 else ''
                            #'undefined2': line[6]
                        }

                        notations.append(notation_dict)

                    else:
                        logging.info(
                            f">>> Skipping line because it is not formatted well. It has only {line_length} columns.")
                        logging.info(f">>> {len(notations)} - {line} ({line_length})")
                        time.sleep(5)

                    previous_line_length = line_length

            logging.info(f"Finished to load {text_quantity} texts. ")
            return pd.DataFrame(notations)
        except FileNotFoundError:
            logging.error(f"File '{self.fileName}.tsv' not found.")
            return None

        except Exception as e:
            logging.error(f"An error occurred while loading notations: {str(e)}")
            return None

    def order_entity_words_by_index(self, df_to_order):

        """
        Order the entity words in a DataFrame based on their index.

        This function assigns a unique entity cardinal number to each group of words that belong to the same entity
        and are in sequence according to their index. The entity cardinal number represents the order of occurrence
        of the entity groups in the DataFrame.

        Args:
            df_to_order (pd.DataFrame): The DataFrame containing the entity words to be ordered.

        Returns:
            pd.DataFrame: The DataFrame with the entity words ordered based on their index and assigned entity cardinal numbers.
        """
        try:
            inSequence = [1]  # Start with index 1
            last_index = df_to_order.index[0]

            df_to_order.loc[last_index, "entity_cardinal"] = str(inSequence[-1])

            for idx in df_to_order.index[1:]:
                if idx == last_index + 1:
                    # Words are in sequence
                    df_to_order.loc[idx, "entity_cardinal"] = str(inSequence[-1])
                else:
                    # Start a new sequence
                    inSequence.append(inSequence[-1] + 1)
                    df_to_order.loc[idx, "entity_cardinal"] = str(inSequence[-1])
                last_index = idx

            logging.info(f">>> List of cardinal entities for each word group: \n{inSequence}")

            return df_to_order

        except Exception as e:
            logging.error(f"An error occurred while ordering entity words: {str(e)}")
            return None

    def concatenate_word_entity(self, df_to_concatenate):

        """
        Concatenate words based on entity attributes in a DataFrame.
        Args:
            df_to_concatenate (pd.DataFrame): The DataFrame containing the words and entity attributes.
        Returns:
            pd.DataFrame: A new DataFrame with concatenated words based on entity attributes.
        """
        try:
            df_to_concatenate['concat_ent'] = \
            df_to_concatenate.groupby(['text', 'entity', 'category_entity', 'entity_cardinal'])['word'].transform(' '.join)
            df_to_concatenate = df_to_concatenate[
                ['text', 'entity', 'category_entity', 'entity_cardinal', 'concat_ent']].drop_duplicates()

            return df_to_concatenate

        except Exception as e:
            logging.error(f"An error occurred while ordering entity words: {str(e)}")
            return None

    def add_column_filename(self, df_to_add_column):
        try:
            logging.info(f"Adding column with {self.fileName} value.")

            df_to_add_column.insert(0, "file_name", self.fileName)

            return df_to_add_column
        except Exception as e:
            logging.error(f"An error occurred while adding column with filename: {str(e)}")

    def write_csv_old(self, df_to_write, filename):

        """
        Write DataFrame to a CSV file.
        Args:
            df_to_write (pd.DataFrame): The DataFrame to be written to the CSV file.
        """

        root_dir = os.path.dirname(os.path.abspath(__file__))
        ct = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")
        file_path = os.path.join(root_dir, '..', 'data/ParsedData', f'{filename}_{ct}_parsed.csv')
        logging.info(f">>> Writing CSV File on {file_path}")

        df_to_write.sort_values(by=['file_name','entity']).to_csv(file_path, sep=';', encoding='utf-8-sig', index=False)

    def write_csv(self, df_to_write, filename):
        """
        Write DataFrame to a CSV file using chunking.
        Args:
            df_to_write (pd.DataFrame): The DataFrame to be written to the CSV file.
            filename (str): Name of the output file.
        """
        root_dir = os.path.dirname(os.path.abspath(__file__))
        ct = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")
        file_path = os.path.join(root_dir, '..', 'data/ParsedData', f'{filename}_{ct}_parsed.csv')
        logging.info(f">>> Writing CSV File on {file_path}")
        logging.info(f"Size of CSV: {len(df_to_write)}")
        logging.info(f"Quantity columns: {len(df_to_write.columns)}")

        chunk_size = 50  # Define your desired chunk size here

        # Sort the DataFrame before chunking
        # sorted_df = df_to_write.drop("text_concat", axis=1).sort_values(by=['file_name', 'entity'])
        sorted_df = df_to_write.sort_values(by=['file_name', 'entity'])
        sorted_df['text_concat'] = sorted_df['text_concat'].str.replace('\r', '')

        # Calculate the number of chunks
        num_chunks = len(sorted_df) // chunk_size + 1
        logging.info(f"Number of chunks: {len(df_to_write.columns)}")


        # Write the DataFrame to the CSV file in chunks
        #with open(file_path, 'w', encoding='utf-8-sig') as f:
        for i in range(num_chunks):
            logging.info(f"Writing chunk number {i}")
            start_idx = i * chunk_size
            end_idx = (i + 1) * chunk_size
            logging.info(f"Start index chunk {i} : {start_idx}")
            logging.info(f"End index chunk {i} : {end_idx}")
            chunk = sorted_df.iloc[start_idx:end_idx]
            logging.info(f"Length of Chunk: {len(chunk)}")
            filenamechunk = f"{filename}_{i}"
            file_path = os.path.join(root_dir, '..', 'data/ParsedData', f'{filenamechunk}_{ct}_parsed.csv')
            #chunk.to_csv(filenamechunk, sep=';', encoding='utf-8-sig', index=False, header=(i == 0))
            chunk.sort_values(by=['file_name', 'entity']).to_csv(file_path, sep=';', encoding='utf-8-sig',
                                                                       index=False)

        logging.info(">>> CSV File writing complete.")

    def concatenate_word_and_text(self, df_to_concatenate):

        """
        Concatenate entities and text based on entity attributes in a DataFrame.
        Args:
            df_to_concatenate (pd.DataFrame): The DataFrame containing the words and entity attributes.
        Returns:
            pd.DataFrame: A new DataFrame with concatenated words based on entity attributes.
        """
        try:

            df_to_concatenate['ent_concat'] = \
                df_to_concatenate.groupby(['entity', 'category_entity', 'entity_cardinal'])['concat_ent'].transform(
                ' '.join)

            df_to_concatenate = df_to_concatenate.drop_duplicates()

            df_to_concatenate['text_concat'] = \
                df_to_concatenate.groupby(['entity', 'category_entity', 'entity_cardinal', 'ent_concat'])['text'].transform(' '.join)
                #df_to_concatenate.groupby(['entity', 'category_entity'])['text'].transform(' '.join)

            df_to_concatenate=df_to_concatenate.drop_duplicates()

            df_to_concatenate = df_to_concatenate[['entity', 'category_entity', 'entity_cardinal','ent_concat', 'text_concat']]
            df_to_concatenate = df_to_concatenate.drop_duplicates()

            return df_to_concatenate

        except Exception as e:
            logging.error(f"An error occurred while ordering entity words: {str(e)}")
            return None