#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import pandas as pd


# In[2]:


# Change REP_DIR to the folder containing all repetitions for a block (network condition)
REPS_DIR = "wifi"
os.chdir(REPS_DIR)


# In[3]:


cwd = os.path.abspath('') 
cwd


# In[4]:


repetition_files = os.listdir(cwd) 
repetition_files


# In[5]:


assert(11 == len(repetition_files)) # check that no of repetitions is 11


# In[6]:


def get_aggregated_rep_df(rep_dir):
    os.chdir(f"{cwd}\\{rep_dir}")
    
    # Read data from file 'Aggregated_Results_Batterystats.csv' 
    aggregated_battery_stats = pd.read_csv('Aggregated_Results_Batterystats.csv') 
    
    navigation_timing_df = pd.DataFrame(columns=['headerSize', 'workerTime', 'fetchTime', 
                                            'timeToFirstByte', 'downloadTime', 'totalTime',
                                            'totalLoadTime', 'dnsLookupTime']) # relevant
    fcp_df = pd.DataFrame(columns=['fcp']) # relevant
    fp_df = pd.DataFrame(columns=['fp']) # relevant
    
    for i in range (0, len(aggregated_battery_stats)):
        website = aggregated_battery_stats['subject'].get(i)
        
        perfumejs_path = f"{cwd}\\{rep_dir}\\data\\nexus5x\\{website}\\chrome\\perfume_js\\"
    
        for file in os.listdir(perfumejs_path):
            if os.path.isfile(os.path.join(perfumejs_path, file)):
                if 'navigationTiming_results_' in file:
                    navigation_timing_stats_for_website = pd.read_csv(f"{perfumejs_path}{file}")
                    navigation_timing_df = navigation_timing_df.append(navigation_timing_stats_for_website[:1], sort=False, ignore_index=True)

                if 'fcp_results_' in file:
                    fcp_for_website = pd.read_csv(f"{perfumejs_path}{file}")
                    fcp_df = fcp_df.append(fcp_for_website[:1], sort=False, ignore_index=True)

                if 'fp_results_' in file:
                    fp_for_website = pd.read_csv(f"{perfumejs_path}{file}")
                    fp_df = fp_df.append(fp_for_website[:1], sort=False, ignore_index=True)

    aggregated_rep = pd.concat([aggregated_battery_stats, navigation_timing_df, fcp_df, fp_df], join = 'outer', axis = 1) 
    assert(30==len(aggregated_rep))

    aggregated_rep.to_csv(f"{cwd}\\{rep_dir}\\Aggregated_Results_For_Rep.csv")

    return aggregated_rep


# In[7]:


all_aggregated_reps = pd.DataFrame()

i = 0
for rep_dir in repetition_files:
    aggregated_rep_df = get_aggregated_rep_df(rep_dir)
    
    assert(len(aggregated_rep_df) == 30)
    
    # Add repetition timestamp (corresponds to rep folder name)
    rep_name_df = pd.concat([pd.DataFrame([rep_dir], columns=['timestamp']) for i in range(30)], ignore_index=True)
    
    aggregated_rep_df = pd.concat([aggregated_rep_df, rep_name_df], axis = 1)
    
    # Aggregate repetition df to result df
    old_len = len(all_aggregated_reps)
    all_aggregated_reps = pd.concat([all_aggregated_reps, aggregated_rep_df])
    new_len = len(all_aggregated_reps)
    
    assert(len(all_aggregated_reps) - old_len == 30)


# In[8]:


assert(len(all_aggregated_reps) == 11*30) # 11 repetitions, 30 websites (330)


# In[9]:


all_aggregated_reps.head()


# In[10]:


all_aggregated_reps.to_csv(f"{cwd}\\Aggregated_Reps_Wifi.csv")


# In[ ]:




