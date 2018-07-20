import os
import sys
import json
import numpy as np

def print_state_action_detail(state):
    for action_rewards in sas[state]:
        print state+" "+action_rewards

def check_state(state,min_test_time):
    result_cnt = 0
    for action_rewards in sas[state]:
        result_cnt+=1
    return result_cnt > min_test_time

#update trans probability according to the past test
def update_probability_topn(state,topn):
    topn_sum = 0
    current_state_dis={}
    total_action=[]
    for action_rewards in sas[state]:
        action,reward = action_rewards.split(",")
        sa = state+";"+action
        current_state_dis[sa]=float(reward)
        total_action.append(float(action))
        #print sa

    total_action_mu = np.mean(total_action)
    total_action_sigma = np.std(total_action)

    print "====="
    sorted_actions = sorted(current_state_dis.items(),key=lambda item:float(-1*item[1]))
    #print sorted_actions 
    cur_n=0
    topn_action=[]
    for sa,value in sorted_actions:
        cur_n+=1
        if cur_n<=topn:
            print sa,value,cur_n
            topn_sum+=value
            cur_state , cur_action = sa.split(";")
            ###add importance sampling!!!
            for i in range(topn-cur_n):
                topn_action.append(float(cur_action))
        else:
            break
    print topn_action
    ##update mu and sigma
    mu[state]=np.mean(topn_action,axis=0)
    sigma[state]=np.std(topn_action,axis=0)
    print "update for state "+state+" , mu = "+str(mu[state])+"("+str(total_action_mu)+")"+" , sigma = "+str(sigma[state])+"("+str(total_action_sigma)+")"
    return 


samap={}
samap_average={}
probability_trans={}
action_list=set()
state_set=set()
sas={}
#mu map for state->action
mu={}
#sigma map for state->action
sigma={}

for line in sys.stdin:
    jasondata = json.loads(line)
    #print jasondata
    try:
        client_type = "client"+jasondata['CLIENT_TYPE']
    except Exception,err:
        print "Read client field error"
        continue

    #print jasondata['IS_CONNECT_WIFI']
    hour = "hour"+jasondata['HOUR']
    weekday = jasondata['WEEKDAY']
    view1h = "view1h"+jasondata['USER_VIEW_1H_ITEMS_NUM']
    view1d =  jasondata['USER_VIEW_1D_ITEMS_NUM']

    view3d = jasondata['USER_VIEW_3D_ITEMS_NUM']
    view1w = jasondata['USER_VIEW_1W_ITEMS_NUM']
    
    reward = jasondata['REWARD']
    #fill in data
    action = jasondata['DDPG_ENSEMBLE_ACTION']
    state = client_type+"_"+hour+"_"+view1h 
    state_set.add(state)
    

    state_action = state+";"+action
    
    if not sas.has_key(state):
        sas[state]=[]
    if not samap.has_key(state_action):
        samap[state_action]=0
        samap_average[state_action]=0
    sas[state].append(action+","+reward)
    k=samap[state_action]
    #calculate average reward in state s when using action a
    samap_average[state_action]=float(samap_average[state_action]*k)/(k+1)+float(reward)/(k+1)
    samap[state_action]+=1
    #sort_and_remain_n()

    #print cols
#print samap
#print samap_average


fully_tested_state_cnt=0
for state in state_set:
    #print state
    #check whether current state is exploid fully: 1.All the action has been tested 2.Each action satisfy minimal test time
    if check_state(state,30):
        #if explore fully, update probability
        print_state_action_detail(state)
        update_probability_topn(state,10)
        fully_tested_state_cnt+=1
    #else:
        #print reason for check_state failed
        #print_state_action_detail(state)

#print probability_trans
print "total state cnt = ",str(len(state_set))," , fully tested cnt = ",str(fully_tested_state_cnt)
