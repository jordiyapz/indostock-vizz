import zipfile
import gdown

from app.helpers.path import PATH


def download_data(file_id):
    print('Downloading data...')
    download_filename = PATH.DATA/'indonesia-stock.zip'

    try:
        gdown.download(id=file_id, output=str(download_filename), resume=True)
    except Exception as ex:
        print(ex)
        return

    with zipfile.ZipFile(str(download_filename), 'r') as zip_ref:
        zip_ref.extractall(str(PATH.DATA/'raw'))
