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
        filename =  "VilaVicosa_NossaSenhoraDaConceicão.revista.normalizada;VilaVicosa_Pardais.revista.normalizada;" \
                    "VilaVicosa_SantaAnaDeBencatel.revista.normalizada;VilaVicosa_SaoBartolomeu.revista.normalizada;" \
                    "VilaVicosa_SaoRomao.revista.normalizada;VilaVicosa.NossaSenhoraDasCiladas.revista.normalisada;" \
                    "Beja_Albernoa.modernizada;Beja_Alfundao.modernizada;Beja_Baleizao.modernizada;" \
                    "Beja_Beringel.modernizada;" \
                    "Beja_Brissos.modernizada;Beja_Farinho.modernizada;" \
                    "Beja_Marmelar.modernizada;" \
                    "Beja_Mombeja.modernizada;Beja_OriolaDeBaixo.modernizada;" \
                    "Beja_Peroguarda.modernizada;Beja_Quintos.modernizada;Beja_Salvada.modernizada;" \
                    "Beja_Salvador.modernizada;Beja_SantaCatarinaDeSelmes.modernizada;" \
                    "Beja_SantaClaraDoLouredo.modernizada;Beja_SantaMaria.modernizada;Beja_SantaVitoria.modernizada;" \
                    "Beja_Santiago.modernizada;Beja_SantissimaTrindade.modernizada;Beja_SaoJoaoBaptista.modernizada;" \
                    "Beja_SaoMatias.modernizada;Beja_SaoPedroDePedrogao.modernizada;Beja_SaoPedroDePomares.modernizada;" \
                    "Beja_SenhoraDaLuz.modernizada;Beja_Vidigueira.modernizada;Beja_VilaDeFrades.modernizada;" \
                    "Beja_Vilalva.modernizada;Beja_VilaRuiva.modernizada;Beja_VilasBoas.modernizada;" \
                    "Evora_NossaSenhoraDaBoaFe_normalizada.revista;Evora_NossaSenhoraDaGracaDoDivor_normalizada.revista;" \
                    "Evora_NossaSenhoraDaMachede.normalisada.revista;Evora_NossaSenhoraDaTourega.normalisada.revista;" \
                    "Evora_Santiago.normalizada.revista;Evora_SantoAntao.normalizada;Evora_SaoBentoDePomares.normalizada;" \
                    "Evora_SaoBentoDoMato.normalizada;Evora_SaoBrasDeRegedouro.normalizada;Evora_SaoJordao.normalizada;" \
                    "Evora_SaoMamede.normalizada;Evora_SaoMancos.normalizada;Evora_SaoMarcosDaAbobada.normalizada;" \
                    "Evora_SaoMatias.normalizada;Evora_SaoMiguelDeMachede.normalizada;Evora_SaoPedro.normalizada;" \
                    "Evora_SaoSebastiaoDaGiesteira.normalizada;Evora_SaoVicenteDeValongo.normalizada;" \
                    "Evora_SaoVicenteDoPigeiro.normalizada;Evora_Se.modernizada.revista;" \
                    "Portalegre_Urra.normalisadaRevista;Portalegre_SaoMartinho.normalisadaRevista" \
                    ";Portalegre_SaoLourenco.normalizada.revista;Portalegre_SaoJuliao.normalizada.revista" \
                    ";Portalegre_SantiagoMaior.normalisada.revista;Portalegre_SantaMariaMadalena.normalizada.revista" \
                    ";Portalegre_Reguengo.normalisada.revista;Portalegre_NossaSenhoraDaAssuncao.Se.revista.normalizada" \
                    ";Portalegre_NossaSenhoraDaAlagoa.normalisada.revista;Portalegre_Fortios.normalisada.revista" \
                    ";Portalegre_Carreiras_normalizada.comParatexto;Portalegre_Caiola_normalizada.revista" \
                    ";Portalegre_Alegrete_modernizada.revista;Portalegre_ RibeiraDeNisa.normalisada.revista1"

        main(filename)
        # print("Por favor, forneça o nome do arquivo como argumento.")