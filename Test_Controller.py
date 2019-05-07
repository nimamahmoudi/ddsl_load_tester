#%%
import time
import pandas as pd
import padasip as pa 
import sys
import time
import numpy as np
import math
from kubernetes import client, config

config.load_kube_config()
set_replica_num(1)


#%%
DEPLOYMENT_NAME = 'pyfibo'
DEPLOYMENT_NS = 'openfaas-fn'


api_instance = client.ExtensionsV1beta1Api()

def get_replica_and_ready():
    api_response = api_instance.read_namespaced_deployment(DEPLOYMENT_NAME, DEPLOYMENT_NS)
    return api_response.status.replicas, api_response.status.ready_replicas

def set_replica_num(rnum):
    rnum = int(rnum)
    if rnum < 1:
        rnum = 1
    api_response = api_instance.read_namespaced_deployment(DEPLOYMENT_NAME, DEPLOYMENT_NS)
    api_response.spec.replicas = rnum
    api_instance.patch_namespaced_deployment_scale(DEPLOYMENT_NAME, DEPLOYMENT_NS, api_response)
    
print(get_replica_and_ready())

#%% Controller section
f = pa.filters.FilterRLS(n=1, mu=0.2, w="random")


# Control Initialization
u_pre = 1
alpha_pre = 0.1
t_pre = 0.0
t_new = 0.0
pole = 0.01
r_setpoint = 100

# Control Logic Func
def simple_control(t_new,r_setpoint,u_pre,pole,alpha_new):
    error_new = -(r_setpoint - t_new)
    u_new = (u_pre) + (((1-pole)/alpha_new)*error_new)
    if u_new<=1:
        u_new = 1
    return u_new 



#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
import os
try:
	os.chdir(os.path.join(os.getcwd(), 'examples'))
	print(os.getcwd())
except:
	pass
import ddsl_load_tester as load_tester


#%%
def custom_sensing():
    r1,r2 = get_replica_and_ready()
    return {'r1':r1 , 'r2':r2}

lt.custom_sensing = custom_sensing
# Testing the function
lt.custom_sensing()
from tqdm.auto import tqdm
tqdm.pandas()

loop_timer = load_tester.TimerClass()
total_timer = load_tester.TimerClass()

user_sequence = [50,100,500,1000,500,100,50]
lt = load_tester.DdslLoadTester(hatch_rate=100, temp_stat_max_len=5, base='http://localhost:8089/')
lt.custom_sensing = custom_sensing
lt.change_count(user_sequence[0])
lt.start_capturing()

loop_time_in_secs = load_tester.get_loop_time_in_secs('10s')

loop_timer.tic()
total_timer.tic()
results = None
for i in tqdm(range(len(user_sequence)*6)):
	user_count = user_sequence[math.floor(i/6)]
	lt.change_count(user_count)

	time.sleep(loop_time_in_secs - loop_timer.toc())
	
	loop_timer.tic()
	
	result = lt.get_all_stats()
	df_result = pd.DataFrame(data=result)
		
	if results is None:
		results = df_result
	else:
		results = results.append(df_result)
	#####Identification
	d = np.array(result['avg_response_time'][-1])
	y, e, w = f.run(d+ np.random.normal(0, 0.000000001, (1, 1)),result['custom_r2'][-1]+ np.random.normal(0, 0.0000000001, (1, 1)))
	alpha_pre= w
	if result['custom_r1'][-1]==result['custom_r2'][-1] :
		u_pre = simple_control(result['avg_response_time'][-1],r_setpoint,u_pre,pole,alpha_pre)
	# Set the number of replicas
		if u_pre >= 110 :
			u_pre = 110
		set_replica_num((u_pre))
lt.stop_test()

results, filename = lt.prepare_results_from_df(results)

results.head()


#%%
res = results

import matplotlib.pyplot as plt

get_ipython().run_line_magic('matplotlib', 'inline')

plt.figure(figsize=(8,18))
plt.subplot(511)
plt.plot(res['elapsed_min'], res['min_response_time'], label='min_response_time')
plt.plot(res['elapsed_min'], res['current_response_time_percentile_50'], label='median_response_time')
plt.plot(res['elapsed_min'], res['avg_response_time'], label='avg_response_time')
plt.plot(res['elapsed_min'], res['current_response_time_percentile_95'], label='95th percentile')
plt.plot(res['elapsed_min'], res['max_response_time'], label='max_response_time')

plt.xlabel('Time (minutes)')
plt.ylabel('Average Response Time (ms)')
plt.legend()

plt.subplot(512)
plt.plot(res['elapsed_min'], res['user_count'])
plt.xlabel('Time (minutes)')
plt.ylabel('Num of Users')

plt.subplot(513)
plt.plot(res['elapsed_min'], res['total_rps'])
plt.xlabel('Time (minutes)')
plt.ylabel('Throughput (req/s)')

plt.subplot(514)
plt.plot(res['elapsed_min'], res['fail_ratio'])
plt.xlabel('Time (minutes)')
plt.ylabel('Fail Ratio')

filename = filename.replace('.csv', '')
plt.savefig(filename + '.png', dpi=300)
plt.savefig(filename + '.pdf')
plt.show()
plt.subplot(515)
plt.plot(res['elapsed_min'], res['custom_r1'])
plt.plot(res['elapsed_min'], res['custom_r2'])
plt.xlabel('Time (minutes)')
plt.ylabel('Custom Value')




#%%
