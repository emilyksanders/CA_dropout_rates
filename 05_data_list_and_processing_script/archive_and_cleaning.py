### Imports ###
import os
import pandas as pd
from waybackpy import WaybackMachineSaveAPI
import re
import time
# import archive_and_cleaning_functions.py --- something like that. 
# define functions elsewhere and then import them to here
# so that this script can be a lot shorter and easier to read

#########################################
############ !! IMPORTANT !! ############
##### RUN FUNCTIONS SCRIPT FIRST!!! #####
############ !! IMPORTANT !! ############
#########################################

### Set WD ###
get_dfs_wd()

### Get the user agent ###
# (we don't need this just yet, but input() is annoying)
user_agent = input('Who is working on this right now? \n')

### Convert user agent (can run as blocks now) ###
user_agent = user_agent.lower()
    
### Import the list ###
dfs = pd.read_csv('dfs_list.csv')
dfs.shape

### Define start_num ###
if dfs['id'].notna().sum()==0:
  start_num = 1
else:
  start_num = max(dfs['id'])+1

### Define categories (e.g., group DFs) ###
dfs['source_var'] = [
  re.match(r'^([A-Za-z]+)', u.split('/')[-1].split('.')[0])[0] 
  for u in dfs['original_url']]
  
### Define ID numbers ###
source_vars = list(dfs['source_var'].unique())

# seed a dictionary
var_dict = {'1': 'chronicabsenteeism'}

# find which ones need an ID
for var in source_vars:
  if var in var_dict.values():
    continue
  else:
    # put it in the dictionary
    var_dict[str(start_num)] = var
    start_num += 1

# get a backwards copy too
var_dict_rev = {v:k for k, v in var_dict.items()}

# assign the numbers
dfs = assign_ids(dfs, source_vars, var_dict_rev)


### Archive them with the Wayback Machine ###
dfs = archive(dfs)

### JIC, specify where to pull from. ###
pull_urls = get_pull_urls(1) # change to 0 for originals

### Create some containers
orig_col_names = {}


### For each df
for url in pull_urls:

###  # Get it in and see what it's about

###  # Get its name
  name = url.split('/')[-1]
  name = name.split('.')[0]
  print('')
  print('='*15)
  print(name)

###  # Load it - let's see what we've got for seps
  failed_attempts = 0
  seps = ['\t', ',', ';']
  for s in seps:
    try: 
      df = pd.read_csv(url, low_memory = False, 
        encoding_errors='replace', sep = s)
      if not df.isna().all().all():
        print(s)
        break
    except Exception as e:
      print(url)
      print(e)
      failed_attempts+=1
      continue
  
 if failed_attempts==len(seps):
   print('none of the seps worked.')
   continue

###  # Save and show some information
  orig_col_names[name] = list(df.columns)
  print('')
  print(list(df.columns), flush = True)

###  # Define a DF ID# for a suffix
  cond = dfs[pull_urls==url].index
  df_id = int(dfs.loc[cond[0], 'id'])

###  # Reformat column names
  # create a container
  new_col_names = []
  
  # for every column name
  for i in list(df.columns):
    title_case = re.search(r'[a-z][A-Z]', i) # first check for TitleCase
    while title_case != None: # gotta get 'em all!
      letters = title_case[0] # yank the letters out of the object
      i = i.replace(letters, letters[0]+'_'+letters[1].lower()) # insert _
      title_case = re.search(r'[a-z][A-Z]', i) # check again
    # once all the TitleCases are gone, do the reformatting that 
    # used to be in the list comp, and append it to that list
    new_col_names.append(f"{i.lower().replace(' (', '--').replace(' ', '_').replace(')', '')}__df{str(df_id).zfill(2)}")
    
  # check my work, reassign that list to be the new column names
  if len(list(df.columns))==len(new_col_names):
    df.columns = new_col_names
  else:
    print(f'wrong number of columns after reformatting for df_id: {df_id}, {url}')
    break

###  # Clear the console for this next bit
  clear()

###  # Print all column names
  print(df.columns, flush = True)

###  # Filtering #  ###

###  # Any chance this could be easy?
  # identify aggregation columns
  agg = 'cats'
  agg_cols = []
  while agg.lower() != 'done':
    agg = input("""
      If any of those columns are a 'level of aggregation' 
      column, enter its name.  One at a time, please.  When 
      you are done, or if there are none, enter 'Done.'
      """)
    if agg in list(df.columns):
      # pick the level
      print(df[agg].value_counts(dropna = False), flush = True)   # may have to wait for this
      level = input('Which of these levels do you want? \n\n')
      # narrow the df
      df = df[df[agg]==level]
      # sanity check
      print('', flush = True)
      print(df[agg].value_counts(dropna = False), flush = True)
      # set these guys up for dropping
      agg_cols.append(agg)
    else:
      continue 
###  # Specify "master" columns
  # create a dictionary container
  merge_cols = {}
  
  # district
  x = master_cols(df, 'district')
  merge_cols[x[0]] = x[1]
  
  # year
  x = master_cols(df, 'year')
  merge_cols[x[0]] = x[1]
  
  # check my work and remove the suffixes
  if df.rename(columns = merge_cols).shape == df.shape:
    df.rename(columns = merge_cols, inplace = True)
  else:
    print(f'something is wrong in the master column section for df_id: {df_id}, {url}')
    break

###  # Specify the columns to "flatten" (i.e., the descriptive columns)
  print('')
  desc_cols = input('Which are the descriptive columns (to flatten)? \n\n')
  desc_cols = desc_cols.split(',')

###  # Specify the columns to preserve (i.e., the informative columns)
  print('')
  info_cols = input('Which are the informative columns (the data)? \n\n')
  info_cols = info_cols.split(',')

###  # Drop all other columns
  # everyone else goes on this list
  drop_cols = [col for col in list(df.columns) if (
    (col not in merge_cols.values()) and
    (col not in desc_cols) and
    (col not in info_cols) )]
  # create a toggle
  drop_inplace = False
  # edit the list as needed
  while drop_inplace == False:
    print(drop_cols)
    print("""
    Would you like to drop these columns? Enter Yes to proceed, 
    Add to add to the list, or Remove to remove from the list.
    """)
    drop_confirm = input()
    
    if drop_confirm.lower()=='yes':
      drop_inplace = True
    elif drop_confirm.lower()=='add':
      add_cols = input('Enter any additional columns to drop. \n\n')
      add_cols = add_cols.split(',')
      drop_cols.extend(add_cols)
    elif drop_confirm.lower()=='remove':    
      remove_cols = input('Enter any columns to NOT drop. \n\n')
      remove_cols = remove_cols.split(',')
      drop_cols = [col for col in drop_cols if col not in remove_cols]
    else:
      print('You have entered an invalid string. Please try again.')
    
  # when that's done (the list of columns to drop is complete)
  df.drop(columns = drop_cols, inplace = drop_inplace)
    
###  # For each descriptive column
  for col in desc_cols:

###  #   # Create a container list that will hold all the sub_dfs
    sub_list = []

###  #   # Specify a descriptive suffix for the overall column
    print(f"""
    The current column is {col}. 
    What is its overall suffix?
    """)
    suf1 = input('Enter suffix: \n\n')

###  #   # Specify descriptive suffixes for each level
    col_vals = list(df[col].unique())
    
    suffixes = input(f""" \
    \n {col} has the following levels: \
    \n {col_vals} \
    \n \
    \n Please enter a list of suffixes corresponding to each \
    \n of those values. Separate each suffix with a comma. Do \
    \n NOT wrap the suffixes in quotation marks, and do NOT use \
    \n any characters that do not belong in column names. \
    \n \
    \n Enter suffixes: \
    \n """)
    
    # clean up that input
    suffixes = suffixes.split(',')
    suffixes = [s.strip() for s in suffixes]
    # and JIC
    suffixes = [f"{i.lower().replace(' (', '--').replace(' ', '_').replace(')', '')}" 
      for i in suffixes]
      
    ### create a dictionary of suffixes
    
    # create a container
    suffix_dict = {}
    # fill it
    for i, j in list(zip(col_vals, suffixes)):
      print(i, j)
      suffix_dict[i] = j

###  #  Do the stuff to it

# set up a counter to keep track of 
    for i in col_vals:    

###  #   # Pull out the right topic-suffix
      suf2 = suffix_dict[i]

###  #   # Split the df apart by these levels
      sub_df = df[df[col]==i]
      
###  #   # Apply suffixes to the informative columns
      new_sub_col_names = [f'{c}-{suf1}-{suf2}' if (c in info_cols) else c for c in sub_df.columns]
      
      # check my work
      if len(new_sub_col_names)==sub_df.shape[1]:
        sub_df.columns = new_sub_col_names
      else:
        print(f'''something is broken assigning col names to a sub_df.\
        \n df_id: {df_id} \
        \n col: {col} \
        \n col_val level: {i} \
        \n suf1: {suf1} \
        \n suf2: {suf2} \
        \n current names: {list(sub_df.columns)}, shape: {sub_df.shape} \
        \n new names: {new_sub_col_names}, length: {len(new_sub_col_names)} \
        \n Ending operation now.''')
        break
        
###  #   # Delete the original descriptive column
      # safety first
      old_shape = sub_df.shape
      new_shape = sub_df.drop(columns = [col]).shape
      if ((old_shape[0]==new_shape[0]) and (old_shape[1]==(new_shape[1]-1))):
        sub_df.drop(columns = [col], inplace = True)
      else:
        print(f'''something is broken dropping a desc column.\
        \n df_id: {df_id} \
        \n col: {col} \
        \n col_val level: {i} \
        \n suf1: {suf1} \
        \n suf2: {suf2} \
        \n current names: {list(sub_df.columns)}, shape: {sub_df.shape} \
        \n new names: {sub_df.drop(columns = [col]).columns}, shape: {sub_df.drop(columns = [col]).shape} \
        \n Ending operation now.''')
        break

###  #   # storage the sub_df to be remerged later



###  #   # Merge the separate DFs back together on 
###  #   # ###  all remaining descriptive columns
  
# save some of the interactive stuff to a JSON
# save it as a dictionary - i.e., 
# 'reporting_category__dfX' -> 'type' every time

# ###  # Any chance this could be easy?  -- TAKE 1
#   agg_cols = [col for col in list(df.columns) if 
#     ((re.search('aggregat', col)) or (re.search('level', col)))]
#   if len(agg_cols)>0:
#     # show what we've got
#     print(agg_cols)
#     print('')
#     # check them out
#     agg = input("""
#     If any of those columns are a 'level of aggregation' 
#     column, enter its name.  Otherwise, just hit enter.
#     """)
#     # proceed with that info
#     if (agg in list(df.columns)):

  # try: 
  #   df = pd.read_csv(url, low_memory = False, 
  #     encoding_errors='replace', sep = '\t')
  #   print('tab')
  # except:
  #   try: 
  #     df = pd.read_csv(url, low_memory = False, 
  #       encoding_errors='replace', sep = ',')
  #     print('comma')
  #   except:
  #     try: 
  #       df = pd.read_csv(url, low_memory = False, 
  #         encoding_errors='replace', sep = ';')
  #       print('semi-colon')
  #     except: 
  #       print('failed to load')
  #       continue
  
  
# assigning ID scraps
# for i in dfs.loc[cond, 'id'].index:
#   dfs.loc[i, 'id'] = start_num
#   start_num += 1
# 
#     
#     # define the conditions
#     # define condition 1 (no id number)
#     cond1 = dfs[dfs['id'].isna()].index
#     # define condition 2 (correct source_var)
#     cond2 = dfs[dfs['source_var']==var].index
#     # define the intersection (both conds = True)
#     cond = list(set(cond1).intersection(cond2))
#     # put it in order, JIC
#     cond.sort()

  #### TAKE THE SUFFIX OFF OF THE ONES WE'RE MERGING ON ####
  
  ## take 1 VVV  ##
  # # define the types of columns that we're probably after
  # merge_col_names = ['academic_year', 'year', 'school_year', 
  #   'district', 'district_code', 'school_district']
  # # look for them
  # merge_cols = {'seed': 'dictionary'}
  # for i in merge_col_names:
  #   # merge_cols.extend([c.split('__')[0] for c in new_col_names if re.search(i, c)])
  #   merge_cols[c] = c.split('__')[0] for c in new_col_names if re.search(i, c)
