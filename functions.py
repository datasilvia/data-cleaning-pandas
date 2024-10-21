import pandas as pd
from datetime import datetime

def clean_column_names(df):
    """
    Cleans the column names of a DataFrame.
    - Removes spaces from the names.
    - Converts all names to lowercase.
    - Replaces spaces with underscores (_).
    
    Parameters:
    df (pandas.DataFrame): The DataFrame whose columns are to be cleaned.

    Returns:
    pandas.DataFrame: DataFrame with cleaned column names.
    """
    
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.lower()
    df.columns = df.columns.str.replace(" ", "_")
    
    return df




def drop_columns(df: pd.DataFrame, columns_to_drop: list) -> pd.DataFrame:
    """
    Drops specified columns from a DataFrame.

    Parameters:
    df (pd.DataFrame): The input DataFrame from which columns need to be removed.
    columns_to_drop (list): A list of column names to be dropped from the DataFrame.

    Returns:
    pd.DataFrame: A DataFrame with the specified columns removed.
    """

    return df.drop(columns=columns_to_drop)




def filter_recent_dates(df, date_column='date', years=25):
    """
    Converts a date column to datetime format and filters the DataFrame to include only records
    from the last `years` years.
    
    Parameters:
    df (pandas.DataFrame): The DataFrame containing the date column.
    date_column (str): The name of the column containing the dates (default is 'date').
    years (int): The number of years to consider for the filter (default is 25).

    Returns:
    pandas.DataFrame: Filtered DataFrame with dates from the last `years` years.
    """

    df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
    current_year = datetime.now().year
    year_cutoff = current_year - years
    df = df[df[date_column].dt.year >= year_cutoff]
    
    return df




def clean_text_columns(df, column_name):
    """
    Cleans the column of a DataFrame by applying various transformations to standardize and clean the text.
    - Converts all text to lowercase.
    - Fills null values with "not specified".
    - Removes special characters like slashes, ampersands, brackets, parentheses, quotes, commas, and question marks.
    - Removes numbers, dashes, and symbols like < and >.
    - Eliminates isolated single characters and pairs of characters.
    - Strips leading and trailing whitespaces.
    - Replaces multiple spaces with a single space.

    Parameters:
    df (pandas.DataFrame): The DataFrame containing the column to be cleaned.
    column_name (str): The name of the column to be cleaned (default is 'species').

    Returns:
    pandas.DataFrame: The DataFrame with the cleaned species column.
    """
    
    df[column_name] = df[column_name].str.lower()
    df[column_name] = df[column_name].fillna("not specified")
    df[column_name] = df[column_name].str.replace(r'[\\/&]', '', regex=True)
    df[column_name] = df[column_name].str.replace(r'[\[\]()\.\"\'\',?]', '', regex=True) 
    df[column_name] = df[column_name].str.replace(r'\d+', '', regex=True) 
    df[column_name] = df[column_name].str.replace(r'[-<>]', '', regex=True) 
    df[column_name] = df[column_name].str.replace(r'\b\w\s\b|\b\s\w\b', '', regex=True)  
    df[column_name] = df[column_name].str.replace(r'(\b\s\w{2}\b|\b\w{2}\s\b|\b\s\w{2}\s\b)', '', regex=True) 
    df[column_name] = df[column_name].str.strip()  
    df[column_name] = df[column_name].str.replace(r'\s+', ' ', regex=True)  
    df[column_name] = df[column_name].str.replace(r'\b\w\s\b|\b\s\w\b', '', regex=True)  
    df[column_name] = df[column_name].str.replace(r'(\b\s\w{2}\b|\b\w{2}\s\b|\b\s\w{2}\s\b)', '', regex=True) 

    return df





def categorize_age(age):
    """
    Categorizes an age value into defined age groups: 'Child', 'Young', 'Adult', 'Senior', or 'Unknown'.
    - If the age is NaN, it returns 'Unknown'.
    - If the age is less than 16, it returns 'Child'.
    - If the age is between 16 and 30 (inclusive), it returns 'Young'.
    - If the age is between 31 and 65 (inclusive), it returns 'Adult'.
    - If the age is between 66 and 100 (inclusive), it returns 'Senior'.
    - For any other value, it returns 'Unknown'.

    Parameters:
    age (float or int): The age value to categorize.

    Returns:
    str: The age group to which the age belongs ('Child', 'Young', 'Adult', 'Senior', or 'Unknown').
    """
    
    if pd.isna(age):
        return 'Unknown'
    if age < 16:
        return 'Child'
    elif 16 <= age < 31:
        return 'Young'
    elif 31 <= age < 66:
        return 'Adult'
    elif 66 <= age <= 100:
        return 'Senior'
    else:
        return 'Unknown'





def classify_text(text: str, classifications: dict):
    """
    Classifies a given text into predefined categories based on keywords.
    The function checks for specified keywords within the text and returns the corresponding category.
    - Converts the input text to lowercase for case-insensitive matching.
    - Searches for keywords in the text to determine the appropriate category.

    Parameters:
    text (str): The text to classify.
    classifications (dict): A dictionary where each key is a category (str) and 
                            each value is a list of keywords (list of str) that 
                            determine that category.
                            Example:
                            {
                                'Category1': ['keyword1', 'keyword2', 'keyword3'],
                                'Category2': ['keyword4', 'keyword5'],
                                'Category3': ['keyword6', 'keyword7', 'keyword8']
                            }

    Returns:
    str: The classification of the text (based on the keys of the dictionary),
         or returns the original input if it is not a string.
    """
    
    if type(text) is not str:
        return text

    text_lower = text.lower()
    for category, keywords in classifications.items():
        if any(keyword in text_lower for keyword in keywords):
            return category

    return text





def categorize_values(df: pd.DataFrame, column_name: str, defined_values: set, default_value: str = 'other') -> pd.DataFrame:
    """
    Categorizes values in a specified column based on a set of defined values.

    Parameters:
    df (pd.DataFrame): The input DataFrame containing the data.
    column_name (str): The name of the column in which values need to be categorized.
    defined_values (set): A set of values considered as defined. Values not in this set will be assigned the default_value.
    default_value (str): The value to assign to values not present in defined_values. Defaults to 'other'.

    Returns:
    pd.DataFrame: A DataFrame with the specified column's values categorized.
    """
    
    df[column_name] = df[column_name].apply(lambda x: x if x in defined_values else default_value)
    return df


