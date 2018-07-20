import os
import sys
       
def print_state_action_detail(action_list):
    for action in action_list:
        sa = state+"_"+action
        if(samap_average.has_key(sa)):
            print " " + action+" "+str(samap_average[sa])+" "+str(samap[sa])

def check_state(action_list,min_test_time):
    result = 1
    for action in action_list:
        sa = state+"_"+action
        if(samap_average.has_key(sa)):
            #print " " + action+" "+str(samap_average[sa])+" "+str(samap[sa])
            if(samap[sa]<min_test_time):
                result = 0
        else:
            result = 0
    return result

def update_probability_topn(topn):
    sum = 0
    for action in action_list:
        sa = state+"_"+action
        if(samap_average.has_key(sa)):
            #print " " + action+" "+str(samap_average[sa])+" "+str(samap[sa])
            if(samap[sa]<min_test_time):
                result = 0
        else:
            result = 0
    return result



samap={}
samap_average={}
action_list=set()
state_set=set()
for line in open("part-00000"):
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
    
    state_action = state+"_"+action
    
    action_list.add(action)
    state_set.add(state)
    
    if not samap.has_key(state_action):
        samap[state_action]=1
        samap_average[state_action]=0
    k=samap[state_action]
    #calculate average reward in state s when using action a
    samap_average[state_action]=float(samap_average[state_action]*k)/(k+1)+float(reward)/(k+1)
    samap[state_action]+=1
    #sort_and_remain_n()

    #print cols
print samap
print samap_average
for state in state_set:
    print state
    #check whether current state is exploid fully: 1.All the action has been tested 2.Each action satisfy minimal test time
    if check_state(action_list,1):
        #if explore fully, update probability
        print_state_action_detail(action_list)
        update_probability_topn(4)
    ##else:
        #print reason for check_state failed
    ##    print_state_action_detail(action_list)

