import requests
from urllib.parse import urlparse
from pathlib import Path
from datetime import datetime

def get_download_url(item, asset_key, headers):
    asset = item.get('assets', {}).get(asset_key, None)
    if asset is None:
        print(f'Asset "{asset_key}" does not exist in this item')
        return None
    r = requests.get(asset.get('href'), headers=headers, allow_redirects=False)
    return r.headers.get('Location')


def download_label(url, output_path, tileid):
    filename = urlparse(url).path.split('/')[-1]
    outpath = output_path / tileid
    outpath.mkdir(parents=True, exist_ok=True)

    r = requests.get(url)
    f = open(outpath / filename, 'wb')
    for chunk in r.iter_content(chunk_size=512 * 1024):
        if chunk:
            f.write(chunk)
    f.close()
    print(f'Downloaded {filename}')
    return


def download_imagery(url, output_path, tileid, date):
    filename = urlparse(url).path.split('/')[-1]
    outpath = output_path / tileid / date
    outpath.mkdir(parents=True, exist_ok=True)

    r = requests.get(url)
    f = open(outpath / filename, 'wb')
    for chunk in r.iter_content(chunk_size=512 * 1024):
        if chunk:
            f.write(chunk)
    f.close()
    print(f'Downloaded {filename}')
    return

# output path where you want to download the data
output_path = Path("data")


ACCESS_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJqa3dNMEpFTURsRlFrSXdOemxDUlVZelJqQkdPRFpHUVRaRVFqWkRNRVJGUWpjeU5ERTFPQSJ9.eyJpc3MiOiJodHRwczovL3JhZGlhbnRlYXJ0aC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU1MzY3NTUzNTE2YTIwZTRlOWNlNjU1IiwiYXVkIjpbImh0dHBzOi8vYXBpLnJhZGlhbnQuZWFydGgvdjEiLCJodHRwczovL3JhZGlhbnRlYXJ0aC5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTgyNTI0MjQ3LCJleHAiOjE1ODMxMjkwNDcsImF6cCI6IlAzSXFMcWJYUm0xMEJVSk1IWEJVdGU2U0FEbjBTOERlIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbXX0.FeR_anORcnnLF-44De7tC9LptpAf4eeRctPhwUFLyGnDMDQ-ij-79xABh0lw-2eY5zcDQL5UNR_UDM6ssDfDJeHnPtwljJ7X1lINP_OyPRUvfPqWcSgLCwKQlFlAhpIA8DgfxdMu7N5dxklhwebutGBTpFWfLSvBPKe3bdqsDBUIF4_MNxpdYZLv2WsQQOM04eoTixmLoSTJhx7E_3GRmy1um2tQ9OfdVHhb_w_PAQiAMk9qeG5SqN_YiMhugm99i1uM999MFAYN35rj3yVgrTI-w80ZoNy-Bx_S8qNBZjUexUT5-I9fKE_IpmPBAv2L-vvWiueGZ4uWR8HaSxFWrA'

# these headers will be used in each request
headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Accept':'application/json'
}

# paste the id of the labels collection:
collectionId = 'ref_african_crops_kenya_02_labels'

# these optional parameters can be used to control what items are returned.
# Here, we want to download all the items so:
limit = 100
bounding_box = []
date_time = []

# retrieves the items and their metadata in the collection
r = requests.get(f'https://api.radiant.earth/mlhub/v1/collections/{collectionId}/items', params={'limit':limit, 'bbox':bounding_box,'datetime':date_time}, headers=headers)
collection = r.json()

# This cell downloads all the multi-spectral images throughout the growing season for this competition.
# The size of data is about 1.5 GB, and download time depends on your internet connection.
# Note that you only need to run this cell and download the data once.
for feature in collection.get('features', []):
    for link in feature.get('links', []):
        if link.get('rel') != 'source':
            continue

        r = requests.get(link['href'], headers=headers)
        feature = r.json()
        assets = feature.get('assets').keys()
        tileid = feature.get('id').split('tile_')[-1][:2]
        date = datetime.strftime(datetime.strptime(feature.get('properties')['datetime'], "%Y-%m-%dT%H:%M:%SZ"),
                                 "%Y%m%d")
        for asset in assets:
            download_url = get_download_url(feature, asset, headers)
            download_imagery(download_url, output_path, tileid, date)

for feature in collection.get('features', []):
    tileid = feature.get('id').split('tile_')[-1][:2]

    # download labels
    download_url = get_download_url(feature, 'labels', headers)
    download_label(download_url, output_path, tileid)

    # download field_ids
    download_url = get_download_url(feature, 'field_ids', headers)
    download_label(download_url, output_path, tileid)

# retrieve list of features (in this case tiles) in the collection
for feature in collection.get('features', []):
    assets = feature.get('assets').keys()
    print("Feature", feature.get('id'), 'with the following assets', list(assets))


# retrieve list of features (in this case tiles) in the collection
for feature in collection.get('features', []):
    assets = feature.get('assets').keys()
    print("Feature", feature.get('id'), 'with the following assets', list(assets))
