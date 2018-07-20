import os
import sys
       
def print_state_action_detail(state,action_list):
    for action in action_list:
        sa = state+";"+action
        if(samap_average.has_key(sa)):
            print " " + action+" "+str(samap_average[sa])+" "+str(samap[sa])

def check_state(state,action_list,min_test_time):
    result = 1
    for action in action_list:
        sa = state+";"+action
        if(samap_average.has_key(sa)):
            #print " " + action+" "+str(samap_average[sa])+" "+str(samap[sa])
            if(samap[sa]<min_test_time):
                result = 0
        else:
            result = 0
    return result

#update trans probability according to the past test
def update_probability_topn(state,action_list,topn):
    topn_sum = 0
    current_state_dis={}
    
    sorted_actions = sorted(samap_average.items(),key=lambda item:float(item[1]))
    print "====="
    for action in action_list:
        sa = state+";"+action
        #print state,action
        current_state_dis[sa]=samap_average[sa]
        probability_trans[sa]=0
    sorted_actions = sorted(current_state_dis.items(),key=lambda item:float(-1*item[1]))
   
    cur_n=0
    for sa,value in sorted_actions:
        cur_n+=1
        if cur_n<=topn:
            print sa,samap[sa],value,cur_n
            topn_sum+=value
        else:
            break
    print topn_sum
    cur_n=0
    for sa,value in sorted_actions:
        cur_n+=1
        if cur_n<=topn:
            probability_trans[sa]=current_state_dis[sa]/topn_sum
            print sa,probability_trans[sa]
        else:
            break
    return 



samap={}
samap_average={}
probability_trans={}
action_list=set()
state_set=set()
for line in sys.stdin:
    cols = line.strip().split(";")
    if len(cols)<5:
        continue

    #fill in data
    global_id = cols[0]
    ts = cols[1]
    action = cols[2]
    reward = cols[3]
    endmark = cols[4]
    state = cols[5]
    
    state_action = state+";"+action
    
    action_list.add(action)
    state_set.add(state)
    
    if not samap.has_key(state_action):
        samap[state_action]=0
        samap_average[state_action]=0
    k=samap[state_action]
    #calculate average reward in state s when using action a
    samap_average[state_action]=float(samap_average[state_action]*k)/(k+1)+float(reward)/(k+1)
    samap[state_action]+=1
    #sort_and_remain_n()

    #print cols
print samap
print samap_average

fully_tested_state_cnt=0
for state in state_set:
    ##print state
    #check whether current state is exploid fully: 1.All the action has been tested 2.Each action satisfy minimal test time
    if check_state(state,action_list,1):
        #if explore fully, update probability
        #print_state_action_detail(state,action_list)
        update_probability_topn(state,action_list,4)
        fully_tested_state_cnt+=1
    ##else:
        #print reason for check_state failed
    ##    print_state_action_detail(state,action_list)

print probability_trans
print "total state cnt = ",str(len(state_set))," , fully tested cnt = ",str(fully_tested_state_cnt)
