# testing stuff 

# set up some fake data to try stuff on 
original = pd.DataFrame(
  data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # one year
    [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2], # two races
    [3, 3, 4, 4, 5, 5, 6, 6, 3, 3, 4, 4, 5, 5, 6, 6], # four districts
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1], # gender
    [7, 8, 9, 0, 1, 3, 4, 5, 2, 6, 7, 1, 8, 9, 4, 3]])  # district-year actual data
original = original.transpose()
original.columns = ['year', 'race', 'district', 'gender', 'num_absences']

test1 = pd.DataFrame(
  data = [
    [1, 1, 1, 1, 1, 1, 1, 1], # one year
    [1, 1, 1, 1, 1, 1, 1, 1], # one race
    [3, 3, 4, 4, 5, 5, 6, 6], # four districts
    [0, 1, 0, 1, 0, 1, 0, 1], # gender
    [7, 8, 9, 0, 1, 3, 4, 5]])  # district-year actual data
test1 = test1.transpose()
test1.columns = ['year', 'race', 'district', 'gender', 'num_absences']

test2 = pd.DataFrame(
  data = [
    [1, 1, 1, 1, 1, 1, 1, 1], # one year
    [2, 2, 2, 2, 2, 2, 2, 2], # one race
    [3, 3, 4, 4, 5, 5, 6, 6], # four districts
    [0, 1, 0, 1, 0, 1, 0, 1], # gender
    [2, 6, 7, 1, 8, 9, 4, 3]])  # district-year actual data
test2 = test2.transpose()
test2.columns = ['year', 'race', 'district', 'gender', 'num_absences']

goal = pd.DataFrame(
  data = [
    [1, 1, 1, 1, 1, 1, 1, 1], # one year
    # race column removed
    [3, 3, 4, 4, 5, 5, 6, 6], # four districts
    [0, 1, 0, 1, 0, 1, 0, 1], # gender
    [7, 8, 9, 0, 1, 3, 4, 5],  # RACE 1 district-year actual data
    [2, 6, 7, 1, 8, 9, 4, 3]])  # RACE 2 district-year actual data
goal = goal.transpose()
goal.columns = ['year', 'district', 'gender', 'num_absences-race-1', 'num_absences-race-2'] 
  
# is the split doing what I want it to do?
sub_df_1 = original[original['race']==1] #split
sub_df_2 = original[original['race']==2] #split
sub_df_2 = sub_df_2.reset_index(drop = True) # reset index to 0 so boolean won't complain

# is there anywhere that they're NOT the same?
(sub_df_1!=test1).sum().sum() # should be 0
(sub_df_2!=test2).sum().sum() # should be 0 
# ^^ this line was yelling before I pd.reset_index'ed it

# Yes.  The splitting works.

# Is the renaming working?

  
  
  
  
