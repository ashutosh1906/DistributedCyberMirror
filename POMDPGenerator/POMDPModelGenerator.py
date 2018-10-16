import POMDPSettings
def generate_mode(output_file_name):
    print('\n ********** Output Model in file: %s'%(output_file_name))
    file_pointer = open(output_file_name,'w')
    write_initial_informations(file_pointer)
    write_initial_belief(file_pointer)
    write_state_transition(file_pointer)
    write_observation_matrix(file_pointer)
    write_rewards(file_pointer)
    file_pointer.close()

def write_initial_informations(file_pointer):
    discount_line = 'discount: %s'%(POMDPSettings.DISCOUNT_FACTOR)
    value_line = 'values: reward'
    state_line = 'states: '
    states = ''
    for state in POMDPSettings.state_space:
        states = '%ss%s '%(states,state.primary_key)
    state_line = '%s%s'%(state_line,states)

    action_line = 'actions: '
    actions = ''
    for action_type in POMDPSettings.action_space_objects:
        for action in action_type:
            actions = '%sd%s '%(actions,action.primary_key)
    action_line = '%s%s' % (action_line,actions)

    observation_line = 'observations: '
    observations = ''
    for state in POMDPSettings.state_space:
        observations = '%so%s ' % (observations,state.primary_key)
    observation_line = '%s%s' % (observation_line, states)

    file_pointer.write('%s\n%s\n%s\n%s\n%s\n\n'%(discount_line,value_line,state_line,action_line,observation_line))

def write_initial_belief(file_pointer):
    belief_line = 'start: '
    for state in POMDPSettings.state_space:
        belief_line = '%s%s '%(belief_line,state.belief)
    file_pointer.write('%s\n\n'%(belief_line))

def write_state_transition(file_pointer):
    for defense_action_type in POMDPSettings.action_space_objects:
        for defense_action in defense_action_type:
            defense_id = defense_action.primary_key
            defense_line = 'T:d%s\n'%(defense_id)
            # print(POMDPSettings.state_transition_pomdp[defense_action.primary_key])
            for old_state in POMDPSettings.state_space:
                old_state_id = old_state.primary_key
                each_old_state_to_new_state = ''
                for new_state in POMDPSettings.state_space:
                    new_state_id = new_state.primary_key
                    if new_state_id not in POMDPSettings.state_transition_pomdp[defense_id][old_state_id]:
                        each_old_state_to_new_state = '%s%s '%(each_old_state_to_new_state,0.0)
                    else:
                        each_old_state_to_new_state = '%s%s ' % (each_old_state_to_new_state,POMDPSettings.state_transition_pomdp[defense_id][old_state_id][new_state_id])
                defense_line = '%s%s\n'%(defense_line,each_old_state_to_new_state)
            file_pointer.write('%s\n'%(defense_line))

def write_observation_matrix(file_pointer):
    for action in POMDPSettings.observation_probability:
        # print(POMDPSettings.observation_probability[action])
        if action==POMDPSettings.WILDCARD_SYMBOL:
            observation_line = 'O:*\n'
        else:
            observation_line = 'O:%s\n'%(action)
        for old_state_id in POMDPSettings.observation_probability[action]:
            each_state_to_observation = ''
            for observation in POMDPSettings.observation_probability[action][old_state_id]:
                each_state_to_observation = '%s%s '%(each_state_to_observation,
                                                     POMDPSettings.observation_probability[action][old_state_id][observation])
            observation_line = '%s%s\n'%(observation_line,each_state_to_observation)
        file_pointer.write('%s\n'%(observation_line))

def write_rewards(file_pointer):
    for old_state_id in POMDPSettings.rewards_pomdp:
        for new_state_id in POMDPSettings.rewards_pomdp[old_state_id]:
            for defense_id in POMDPSettings.rewards_pomdp[old_state_id][new_state_id]:
                for observation in POMDPSettings.rewards_pomdp[old_state_id][new_state_id][defense_id]:
                    if observation==POMDPSettings.WILDCARD_SYMBOL:
                        reward_line = 'R: d%s : s%s : s%s : * '%(defense_id,old_state_id,new_state_id)
                    else:
                        reward_line = 'R: d%s : s%s : s%s : o%s '%(defense_id,old_state_id,new_state_id,observation)
                    reward_line = '%s%s\n'%(reward_line,
                                          POMDPSettings.rewards_pomdp[old_state_id][new_state_id][defense_id][POMDPSettings.WILDCARD_SYMBOL])
                    file_pointer.write('%s'%(reward_line))