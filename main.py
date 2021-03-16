import logging
import pandas as pd
import google_drive as gdrive
import utils

def main():

    utils.setLogs('wiser', loglevel=logging.INFO)

    gdrive_instance = gdrive.connect()

    files = gdrive.find_files(gdrive_instance, filename = 'acervo')

    dataframes = []

    for file in files:

        downloaded_file = gdrive.download_file(gdrive_instance, file)
        logging.info(f'Criando dataframe do arquivo {file["name"]}')
        downloaded_dataframe = utils.sendFiletoDF(downloaded_file)
        dataframes.append(downloaded_dataframe)

    logging.info('Concatenando todos os dataframes')
    result = pd.concat(dataframes)
    
    
    logging.info('removendo quebras de linha para gerar csv')
    result.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"], value=["",""], regex=True, inplace=True)
    logging.info('criando acervo.csv')
    pd.DataFrame.to_csv(result, 'acervo.csv', index=False, line_terminator='\n',encoding='utf-8')


if __name__ == '__main__':
    main()