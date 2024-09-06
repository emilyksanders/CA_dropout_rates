# stuff from Eli

# URL of the .txt file
url = 'https://www3.cde.ca.gov/demo-downloads/tamo/tamo2.txt'
url = 'https://www3.cde.ca.gov/demo-downloads/attendance/chronicabsenteeism23.txt'

# Read in the url with the delimiter and encoding to deal with special characters
df_iso = pd.read_csv(
  url, delimiter='\t', encoding='ISO-8859-1')
  
df_errors = pd.read_csv(
  url, delimiter='\t', encoding_errors='replace')

pd.set_option('display.max_columns', None)
df
df.loc[(df['Aggregate Level'] == 'D') and 
       (df['Charter School'] == 'All') and 
       (df['DASS'] == 'All') and
       (df['School Grade Span'] == 'All') and 
       (df['Subject Area'] == 'TA')]

for i in list(df_iso.columns):
  if ((df_iso[i].unique().sort())!= (df_errors[i].unique().sort())):
    print(i)

[d for d in df_iso[i].unique() if d not in df_errors[i].unique()]

[d for d in df_errors[i].unique() if d not in df_iso[i].unique()]


import re

[d for d in list(df_iso[i].unique()) if re.search(r'ñ', d)]

list1 = [str(j) for j in list(df_iso[i].unique())]
list2 = [str(j) for j in list(df_errors[i].unique())]
list3 = set(list1).difference(list2)
list4 = set(list2).difference(list1)
print(list(list3))
print(list(list4))

[l for l in list1 if re.search(r'Para Los Ni', l)]
[re.sub(r'Para Los Ni.*s', 'Para Los Ninos', l, flags = re.IGNORECASE) for l in list1 if re.search(r'Para Los Ni', l)]

re.search(r'�', list(list4)[0])

s = "Hello world !!"
":".join("{:02x}".format(ord(c)) for c in s)



