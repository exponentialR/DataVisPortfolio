import pandas as pd

def run(df):
    df['Android_Ver'] = df['Android_Ver'].replace(
    to_replace=[r"([1-8]).*", 'Varies with device'],
    value=[r"\1", "4"],
    regex=True
    )
    nan_ratings = df.loc[df['Rating'].isna()].Category.value_counts()
    for idx, val in nan_ratings.items():
        avg = df.loc[df['Category'] == idx].Rating.mean()
        df.loc[(df['Category'] == idx) & (df['Rating'].isna()), 'Rating'] = avg
    unrated_count = df['Content_Rating'].value_counts().get('Unrated', 0)
    print(f'Unrated count: {unrated_count}')
    df.drop(df[df['Content_Rating'] == 'Unrated'].index, inplace=True)
    df.dropna(inplace=True)

    df['Rating'] = pd.to_numeric(df['Rating'])
    df['Reviews'] = pd.to_numeric(df['Reviews'])
    df[['Android_Ver']] = df[['Android_Ver']].astype(int)
    df['Installs'] = df['Installs'].str.replace(',', '', regex=False)
    df['Installs'] = pd.to_numeric(df['Installs'])

    df['Price'] = df['Price'].str.replace('$', '', regex=False)
    df['Price'] = pd.to_numeric(df['Price'])

    df['Rating'] = df['Rating'].mul(2).round().div(2)

    return df
