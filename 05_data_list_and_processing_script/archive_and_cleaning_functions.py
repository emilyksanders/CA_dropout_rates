### Define Some Helpful Friends ###

#############################
##### Clear the console #####
#############################

# thanks to stackoverflow
# https://stackoverflow.com/questions/517970/how-can-i-clear-the-interpreter-console
clear = lambda: os.system('cls')


##################################################
##### Make sure we're in the right directory #####
##################################################

def get_dfs_wd():
  wd_check = None
  while wd_check != "Yes":
    
    wd_list = ('\n').join(os.listdir())
  
    wd_prompt = f'''
    The current working directory is
    {os.getcwd()}.
    
    It contains
    {wd_list}
    
    If this is the correct directory (i.e., the list of dataframes is
    in it), please enter "Yes," with no punctuation.
    
    If it is not the correct directory, please enter the correct path,
    including any "backup dots" ("..") but WITHOUT QUOTATION MARKS.
    
    '''
    
    wd_check = input(wd_prompt)
    
    if wd_check.lower() != "yes":
      os.chdir(wd_check)
    elif wd_check.lower() == "yes":
      return 'Working directory set.'


##########################################################
##### Assign ID numbers to each variable represented #####
##########################################################

def assign_ids(dfs, source_vars, var_dict_rev):
  ''' Assign ID numbers to the source variables in dfs.
  dfs = the dataframe of data info
  source_vars = the list of variables that need/have IDs
  var_dict_rev = the reversed dictionarty where the variables  
                 are the keys and the numbers are the values
  '''
  for var in source_vars:
    sub_df = dfs[dfs['source_var']==var]
    # if NONE of them are NA (isna = False = 0 -> sum(0)=0), AND all the same
    if ((sub_df['id'].isna().sum()==0) and (len(list(sub_df['id'].unique()))==1)):
      continue
    elif ((sub_df['id'].isna().sum()==0) and (len(list(sub_df['id'].unique()))>1)):
      print(f'Multiple IDs for source_var {var}.')
      break
    elif sub_df['id'].notna().sum()==0: # if NOBODY is populated; ALL are NA
      rows = dfs[dfs['source_var']==var].index
      dfs.loc[rows, 'id'] = int(var_dict_rev[var])
    elif ((sub_df['id'].isna().sum()>0) and (len(list(sub_df['id'].unique()))>2)): # not all NA, some are populated but we have a value, an NA, and a mystery entry
      print(f'Multiple non-NA IDs for source_var {var}.')
      break
    elif ((sub_df['id'].isna().sum()>0) and (len(list(sub_df['id'].unique()))==2)): # not all NA, some are populated; we have a value, an NA, and nothing else
        rows = dfs[dfs['source_var']==var].index
        dfs.loc[rows, 'id'] = int(var_dict_rev[var])
    else:
      print(f'We got to else on {var}; something is broken.')
      break
  return dfs


###########################################
##### Archive URLs to Wayback Machine #####
###########################################

# Archive all not-yet-archived URLs to Wayback Machine (my beloved)
def archive(dfs):

  # define the condition (no archival url)
  cond = dfs['archive_url'].isna()
  
  for i in dfs[cond].index: #[1:]:
    # extra security
    s = str(dfs.loc[i, 'archive_url'])
    if ((s==s.replace(' ', '')) and (re.match(r'https://web.archive.org/web', s) is not None)):
      continue
    # now here we go
    else:
      # define the URL to save
      url = dfs.loc[i, 'original_url']
      # signs of life
      print(url)
  
      # create the save object
      save_api = WaybackMachineSaveAPI(url, user_agent)
      
      # hedge our bets
      try:
        print('trying to save')
        # save it, and gather the output url
        saved_url = save_api.save()
        # put that url in the df
        dfs.loc[i, 'archive_url'] = saved_url
        # collect the timestamp data
        t = save_api.timestamp()
        # put the archive date in the df
        dfs.loc[i, 'archive_date'] = t.strftime('%Y-%m-%d')
        # put the archive time in the df
        dfs.loc[i, 'archive_time_GMT'] = t.strftime('%H:%M')
        # record who did it
        dfs.loc[i, 'user_agent'] = user_agent
      except Exception as e:
        print(e)
        continue
      
      print('')
      
      # be polite to the server
      time.sleep(2)
  
  return dfs


###############################################
##### Specify which list of URLs to clean #####
###############################################

# (Because the archiving wasn't working before, this is a 
# safety valve to ensure the whole thing doesn't just break)
def get_pull_urls():
  done = False
  
  while done == False:
    pull_urls = input('Pull original URLs (0) or archived URLs (1)? \n')
    
    if pull_urls == '0':
      pull_urls = dfs['original_url']
      done = True
    elif pull_urls == '1':
      pull_urls = dfs['archive_url']
      done = True
    else:
      print('Try again, ding dong!')
  
  return pull_urls


##################################################
##### Set "master" district and year columns #####
##################################################

def master_cols(df, col_type):
  '''Identify "master" columns for district and year
  
  Args:
    df (pd.DataFrame) = the df we're looking at
    col_type (str) = which kind of master column we're 
      identifying, either 'district' ('d') or 'year' ('y')
  
  Raise: 
    will quit and yell at you if you give it a bad col_type
  
  Return:
    a TUPLE of of strings:
    (the column name you entered, its unsuffixed name)
  '''
  
  if col_type[0]=='d':
    col_type = 'district'
  elif col_type[0]=='y':
    col_type = 'school year'
  else:
    print("Bad col_type!")
    return None
  
  # flush console
  clear()
  
  # print the options
  print(df.columns)
  
  # create container
  master_col = []
  
  # we're trying to get ONE entry
  while len(master_col)!=1:
    master_col_orig = input('Which column is the "master" {col_type} column? \n\n')
    # make sure dummy didn't enter a list
    master_col = master_col.split(',')
  # if it wasn't a list, then splitting it made it a list of 1. change it back.
  master_col = master_col[0]
  
  # drop the suffix
  master_col = master_col.split('__')[0]
  
  return (master_col_orig, master_col)
  
