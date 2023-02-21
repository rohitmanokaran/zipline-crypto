# based on http://alphacompiler.com
import os
import requests
import numpy as np
import pandas as pd

from zipline.data import bundles
from zipline.pipeline.classifiers import Classifier
from zipline.utils.numpy_utils import int64_dtype

# this gets all the data for the three exchanges 6000+ tickers
BASE_URL = "http://old.nasdaq.com/screening/companies-by-industry.aspx?&render=download"

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
# This list is provided, but you should refresh its content from time to time
RAW_FILE = "companylist.csv"
INPUT_FILE = os.path.join(BASE_PATH, RAW_FILE)
SID_FILE_NAME = "NASDAQ_sids.npy"  # persisted np.array where
SECTOR_PATH = os.path.join(BASE_PATH, SID_FILE_NAME)

# NASDAQ sectors, not the same as Morningstar
SECTOR_CODING = {
    "Basic Industries": 0,
    "Capital Goods": 1,
    "Consumer Durables": 2,
    "Consumer Non-Durables": 3,
    "Consumer Services": 4,
    "Energy": 5,
    "Finance": 6,
    "Health Care": 7,
    "Miscellaneous": 8,
    "Public Utilities": 9,
    "Technology": 10,
    "Transportation": 11,
    "n/a": -1,
}

SECTOR_LABELS = dict(zip(SECTOR_CODING.values(), SECTOR_CODING.keys()))


def get_tickers_from_bundle(bundle_name):
    """Gets a list of tickers from a given bundle"""
    bundle_data = bundles.load(bundle_name, os.environ, None)

    # get a list of all sids
    lifetimes = bundle_data.asset_finder._compute_asset_lifetimes("US")
    all_sids = lifetimes.sid

    # retreive all assets in the bundle
    all_assets = bundle_data.asset_finder.retrieve_all(all_sids)

    # return only tickers
    return dict(map(lambda x: (x.symbol, x.sid), all_assets))


def download_nasdaq_company_list():
    r = requests.get(BASE_URL, allow_redirects=True)
    open(INPUT_FILE, "wb").write(r.content)


def create_sid_table_from_file(bundle_name="alpaca_api"):
    """reads the raw file, maps tickers -> SIDS,
    then maps sector strings to integers, and saves
    to the file: SID_FILE"""
    df = pd.read_csv(INPUT_FILE, index_col="Symbol")
    df = df.drop_duplicates()

    coded_sectors_for_ticker = df["Sector"].map(SECTOR_CODING).fillna(-1)

    ae_d = get_tickers_from_bundle(bundle_name)
    N = max(ae_d.values()) + 1

    # create empty 1-D array to hold data where index = SID
    sectors = np.full(N, -1, np.dtype("int64"))

    # iterate over Assets in the bundle, and fill in sectors
    for ticker, sid in ae_d.items():
        sectors[sid] = coded_sectors_for_ticker.get(ticker, -1)

    np.save(SECTOR_PATH, sectors)


class ZiplineTraderSector(Classifier):
    inputs = ()
    dtype = int64_dtype
    window_length = 0
    missing_value = -1

    def __init__(self):
        create_sid_table_from_file()
        self.data = np.load(SECTOR_PATH)

    def _compute(self, arrays, dates, assets, mask):
        return np.where(
            mask,
            self.data[assets],
            self.missing_value,
        )


if __name__ == "__main__":
    # if you want to refresh the basdaq asset list.
    # download_nasdaq_company_list()
    # get_tickers_from_bundle("alpaca_api")

    create_sid_table_from_file()

    sector = ZiplineTraderSector()
    print(sector.data)
