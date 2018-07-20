import os
import sys

samap={}
samap_average={}
action_list=set()
state_set=set()

for line in open("part-00000"):
     cols = line.strip().split(";")
     if len(cols)<5:
         continue
     global_id = cols[0]
     ts = cols[1]
     action = cols[2]
     action_list.add(action)
     reward = cols[3]
     endmark = cols[4]
     state = cols[5]
     state_action = state+"_"+action
     state_set.add(state)
     if not samap.has_key(state_action):
         samap[state_action]=1
         samap_average[state_action]=0
     k=samap[state_action]
     samap_average[state_action]=float(samap_average[state_action]*k)/(k+1)+float(reward)/(k+1)
     samap[state_action]+=1
     #sort_and_remain_n()
 
     #print cols
print samap
print samap_average
for state in state_set:
     print state
     for action in action_list:
         if(samap_average.has_key(state+"_"+action)):
             print " " + action+" "+str(samap_average[state+"_"+action])
