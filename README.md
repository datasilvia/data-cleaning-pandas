# data-cleaning-pandas
# Sharks Attacks

![logo_ironhack_blue 7](https://user-images.githubusercontent.com/23629340/40541063-a07a0a8a-601a-11e8-91b5-2f13e4e6b441.png)
![Escápate](/images/escapate.jpg "Escápate. Explora el mar a tu ritmo: adrenalina o relax, tú decides")

Welcome to our **Data Wrangling Quest**!
This project is part of the Ironhack Data Analysis bootcamp.
**Our mission**: to clean a really messy data set known as “Shark Attacks” through using data wrangling techniques. 
By doing so we will be able to prepare the data set for analysis for a use case of our choice. 
This dataset contains detailed information on shark attacks but has numerous challenges due to the high number of null values, poorly formatted entries, and typographical errors and misspelled words.


## Approaching the task:

We initially examined the Shark Attack dataset, understood its structure and formulate several hypotheses about the data. 
The Shark Attacks dataset has 6970 rows and 23 columns.
We decided to eliminate several columns that we were not going to use because they were irrelevant for our analysis, such are:
-name, 
-case number, and
-source.

Throughout the project, we have used Python programming and the Pandas library to implement these data cleaning techniques:
- Handling null values.

We used .fillna() to manage null values, replacing them with "not specified" or "unknown".
- Dropping columns.

We dropped the columns that were not necessary for our analysis
- Removing duplicated data.
- Manipulating strings.
- Applying Regex.

We used Regular Expressions (Regex) to eliminate some characters in the data, such as special symbols.
We also made a research on the patterns which might be relevant for some columns on this particular dataset (like patterns in  activity descriptions, etc.).
- Formatting the data
- Grouping data.
- Creating pivot tables.


During the cleaning phase of the dataset we have had to deal with:
-null values and missing values
-duplicates
-spelling errors
-formatting inconsistencies


Once the dataset is cleaned, we used exploratory data analysis (**EDA**) to validate our initial hypotheses and extract meaningful insights.


### Our initial hypothesis were:

- It is easier to be attacked by a shark while doing activities like swimming.

- There are more attacks in summer time because is when more people go on vacation and visit the sea.


 “As a company that sells diving trips, I want to suggest destination for shark spotting”, 
 
 “ As a company that sells surf experiences or surf boards, I want to know where to set up a new shop and avoid shark attacks”.




# Steps taken:


# 1.- **Import the .xls file** into Python.

``` python

url = "https://www.sharkattackfile.net/spreadsheets/GSAF5.xls"
df_sharks = pd.read_excel(url)

```

# 2.- **Examine the data** and try to understand what the fields mean before proceeding with data cleaning and manipulation.

```python

print(df_sharks.shape)
df_sharks.head(5)

```

The Shark Attacks dataset has 6970 rows and 23 columns.


# 3.- Decide on a hypothesis (or hypotheses)/**case use** to guide our data cleaning efforts.

We pretended that a major **travel agency** had hired us to solve their clients' concerns when choosing vacation destinations.
Some wanted to use their vacation for shark watching, and others simply preferred a quiet time on the beach.
For this reason, we decided to investigate where shark sightings would be most possible, and the activities to avoid to stay safe, and also the places where it is most difficult for you to suffer an incident with a shark.

# 4.- **Analyze the structure** and quality of a dataset, identify potential issues or problems, and develop a plan for cleaning and transforming the data according to our needs.

We made a function to **clean the column names**:
We used the .replace() method to change blank spaces for "_"
Then we made all names lower case using the .lower() method to standarize data in categorical columns.

```python

def clean_column_names(df):
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.lower()
    df.columns = df.columns.str.replace(" ", "_")
    return df

```

We decided to **drop some columns** we would not use.

```python

df_sharks = df_sharks.drop(columns=['pdf', 'href_formula', 'href', 'case_number', 'case_number.1',
       'original_order', 'unnamed:_21', 'unnamed:_22', 'unnamed:_11', 'source', 'name'])

```


We managed the **date column** to be in the **correct format**, and kept the data from **the last 25 years**, as we consider that older data might be nos relevant our case.

```python

def filter_recent_dates(df, date_column='date', years=25):
    df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
    current_year = datetime.now().year
    year_cutoff = current_year - years
    df = df[df[date_column].dt.year >= year_cutoff]
    return df

```


 After filtering the dates and dropping columns, the dataset had 2644 rows and 23 columns.

# 5.- **Structure the data** to make it suitable for analysis.  

We made a function to **clean the text** of some of the categorical columns:


```python

def clean_text_columns(df, columns):

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
    
```

# 6.- We treated **each column** independently.

For example, for the **'age' column** we did a mapping to correct misformatted data.
We then **grouped the data** to categorize them into 4 age groups: 'Child', 'Young', 'Adult' and 'Senior':

```python

def categorize_age(age):
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

df_sharks['age_group'] = df_sharks['age'].apply(categorize_age)
df_sharks.insert(9, 'age_group', df_sharks.pop('age_group'))

```


For the **'sex' column** we also used **mapping** to correct misformatted data

For the **'country' column** we used the unidecode to eliminate accents, and then we used also a **mapping** tecnique to correct data.

For the **'injuries' column** we had to replace some values before defining a function to clasify the rest of values. This is made by defining dictionaries to clasify the data.
By using a custom function and mapping dictionary, we were able to handle dozens of common typos and synonyms in a more automated manner.

```python

def clasificar_pupas(pupa : str):
    if type(pupa) is not str:
        return pupa

    clasificaciones = {
        'FATAL': ['fatal', 'severe', 'death'],
        'NO DETAILS': ['question', 'not recov', 'unconfirmed', 'disappeared', 'drow', 'not confirmed', 'remain', 'unknown', 'missing', 'details','?',' '],
        'MAJOR INJURY': ['"mauled"','bit', 'injuries', 'leg', 'thigh', 'face', 'arm', 'rib', 'head', 'torso', 'hip','major'],
        'MINOR INJURY': ['minor', 'lacera', 'abrasi', 'bruis', 'superfi', 'injured','cut', 'calf', 'hand', 'foot', 'shoulder', 'elbow', 'ankle', 'knee', 'finger', 'wrist', 'eye', 'toe', 'lip', 'non-lifethreatening', 'wounds'],
        'NO INJURY': ['"recovered"','recovered','no injury', 'no inury', 'no ijnury', 'no injurty', 'did not', 'otherwise', 'uninjured', 'neither', 'not injur', 'hoax'],
    }

    pupa_lower = pupa.lower()
    for clasificacion, keywords in clasificaciones.items():
        if any(keyword in pupa_lower for keyword in keywords):
            return clasificacion

    return pupa

```


This function was also used in the **'species'** and **'activity' columns**, being undoubtedly a much better approach than the previous one that was being carried out, using endless .replace() methods, and a list of terms to eliminate.



# 7.- We investigate to use **visualizations**.

We used various types of visualizations to start understanding the trends and patterns in the data and to support our findings.

![Map with locations](/images/mapa.jpg Locations with reported sharks attacks)

![Most dangerous activities](/images/actividad.jpg.jpg Activities with high number of attacks reported)
   

# 8.- We prepare a visually appealing presentation to effectively **communicate the insights** and conclusions to stakeholders. 

We made sure building a compelling narrative that highlights the significance of our analysis.

You can find the presentation slides here:  [Data Analysis for Escápate travel agency](https://prezi.com/p/2jnvucoj-bxa/?present=1)

You can also download the .pdf file from this repository.





# Challenges Faced

## High Degree of Data Inconsistency:

One of the most significant challenges was the variety of formats and inconsistencies within the text data, especially in the categorical columns. Each record often contained slight variations that required extensive cleaning and standardization.

## Managing Null Values:

Filling missing data in a way that preserved the overall data quality was challenging. In some cases, it was difficult to determine if a missing value indicated a lack of information or simply an unknown characteristic.

## Balancing Automation and Accuracy:

While using regular expressions and mappings helped speed up the process, ensuring that these automated processes did not overcorrect or misclassify entries required careful validation and manual review.


# Key Learnings

### Importance of Data Cleaning in Analysis:

This project reinforced the critical role of data cleaning in any analysis. Clean data not only improves the accuracy of analytical models but also ensures that insights derived are meaningful and actionable.

### Handling Real-World Datasets:

Working with a real-world dataset like "Shark Attacks" highlighted the complexities that can arise when data is not collected or recorded in a consistent manner. 
It provided valuable experience in handling messy data and applying creative solutions to common data problems.

### Building Reusable Cleaning Functions:

Creating functions to handle repetitive tasks, like text standardization and filling null values, proved invaluable. These functions can be adapted to other datasets, making future data cleaning processes more efficient.


# Conclusion

The analysis and cleaning of the "Shark Attacks" dataset was a **challenging but rewarding** exercise. 
By applying a variety of data cleaning techniques, we were able to transform a highly inconsistent dataset into a more structured and usable form.
This project not only **enhanced our technical skills in data manipulation and cleaning** but also **provided a deeper understanding of the importance of clean data** in drawing accurate insights.













    
