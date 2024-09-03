# stuff from Eli

# URL of the .txt file
url = 'https://www3.cde.ca.gov/demo-downloads/tamo/tamo2.txt'

# Read in the url with the delimiter and encoding to deal with special characters
df = pd.read_csv(
  url, delimiter='\t', encoding='ISO-8859-1')

pd.set_option('display.max_columns', None)
df
df.loc[(df['Aggregate Level'] == 'D') and 
       (df['Charter School'] == 'All') and 
       (df['DASS'] == 'All') and
       (df['School Grade Span'] == 'All') and 
       (df['Subject Area'] == 'TA')]
