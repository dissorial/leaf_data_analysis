import pandas as pd


def get_data(filepath):
    df = pd.read_csv(filepath)
    classes_to_rename = {
        'AP ENG B': 'AP ENG',
        'AP ENG A': 'AP ENG',
        'AP ECON A': 'AP ECON',
        'AP ECON B': 'AP ECON',
        'NL-SK 4A': 'NL SK',
        'NL-SK 3B': 'NL SK',
        'NL-SK 3A': 'NL SK',
        'NL-SK 4B': 'NL SK',
        'CES-WR 3A': 'CES-WR',
        'CES-WR 3B': 'CES-WR',
        'SK as FL 3': 'SK as FL',
        'SK as FL 4': 'SK as FL',
        'LEAF CORE A': 'LEAF CORE',
        'AP SEM 3': 'AP SEM',
        'ELL 3': 'ELL',
        'AP RES 4': 'AP RES',
        'NL-CZ 3+4': 'NL-CZ'
    }

    df['Class'].replace(classes_to_rename, inplace=True)
    return df


def get_classdata(df, input_class, input_terms):
    classdata = df[(df['Class'] == input_class)
                   & (df['Term'].isin(input_terms))]
    return classdata