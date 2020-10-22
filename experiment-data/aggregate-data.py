#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import pandas as pd


# In[2]:


cwd = os.path.abspath('') 
cwd


# In[3]:


files = os.listdir(cwd) 
files


# In[4]:


# Read data from file 'Aggregated_Results_Batterystats.csv' 
aggregated_battery_stats = pd.read_csv('wifi/2020.10.11_192407/Aggregated_Results_Batterystats.csv')
# Preview the first 5 lines of the loaded data 
aggregated_battery_stats.head()


# In[5]:


navigation_timing_df = pd.DataFrame(columns=['headerSize', 'workerTime', 'fetchTime', 
                                            'timeToFirstByte', 'downloadTime', 'totalTime',
                                            'totalLoadTime', 'dnsLookupTime']) # relevant
fcp_df = pd.DataFrame(columns=['fcp']) # relevant
fp_df = pd.DataFrame(columns=['fp']) # relevant
# fid_df = pd.DataFrame(columns=['fid'])
# cls_df = pd.DataFrame(columns=['cls'])
# lcp_df = pd.DataFrame(columns=['lcp'])
# fid_df = pd.DataFrame(columns=['fid'])
# network_information_df = pd.DataFrame(columns=['rtt', 'saveData', 'effectiveType', 'downlink'])
# storage_estimate_df = pd.DataFrame(columns=['usage', 'indexedDB', 'quota', 'caches'])
# tbt_df = pd.DataFrame(columns=['tbt'])


# In[6]:


for i in range (0, len(aggregated_battery_stats)):
    website = aggregated_battery_stats['subject'].get(i)
    perfumejs_path = f"{cwd}\\data\\nexus5x\\{website}\\chrome\\perfume_js\\"
    
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


# In[7]:2020.10.11_192407


assert(i+1==len(navigation_timing_df))
assert(i+1==len(fcp_df))
assert(i+1==len(fp_df))
assert(i+1==len(aggregated_battery_stats))


# In[8]:


navigation_timing_df.head()


# In[9]:


fcp_df.head()


# In[10]:


fp_df.head()


# In[11]:


aggregated_results = pd.concat([aggregated_battery_stats, navigation_timing_df, fcp_df, fp_df], join = 'outer', axis = 1) 
assert(30==len(aggregated_results))


# In[12]:


aggregated_results.head()


# In[13]:


aggregated_results.to_csv('Aggregated_Results_Full.csv')


# In[ ]:




