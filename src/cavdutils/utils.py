from pandas import DataFrame, MultiIndex
import pygeohash as gh
import pandas as pd


output_cols = ['entityid', 'address', 'confidence', 'geohash', 'lat', 'lng', 'source', 'verified']


def normalize_output(df, entity_id):
    if df is None:
        return empty_dataframe(columns=output_cols)

    df = df.assign(
        entityid=entity_id,
        confidence=None,
        verified=False,
        lat=pd.to_numeric(df.lat),
        lng=pd.to_numeric(df.lng)
    )
    df = df.assign(
        geohash=df.apply(lambda row: gh.encode(row.lat, row.lng, precision=5), axis=1),
    )[output_cols]
    return df


def empty_dataframe(index=None, columns=None, dtypes=None):
    """
    Creates an empty DataFrame with proper columns and index names. Useful if callers rely on a certain interface.
    :param index: list of names of the index columns
    :param columns: list of names of the columns
    :param dtypes: dictionary defining desired types for (a subset of) columns
    :return: pd.DataFrame(index=[...index], columns=[...columns])
    """
    return DataFrame(
        [],
        index=MultiIndex.from_tuples([], names=index) if index is not None else None,
        columns=columns
    ).astype(dtypes)
