import POMDPSettings
def generate_model(output_file_name):
    print('\n ********** Output Model in file: %s'%(output_file_name))
    file_pointer = open(output_file_name,'w')
    write_initial_informations(file_pointer)
    write_initial_belief(file_pointer)
    write_state_transition(file_pointer)
    write_observation_matrix(file_pointer)
    write_rewards(file_pointer)
    file_pointer.close()

def generate_model_fast_parsing(output_file_name):
    print('\n ********** Output Model in file: %s' % (output_file_name))
    file_pointer = open(output_file_name, 'w')
    write_initial_informations_fast(file_pointer)
    write_initial_belief(file_pointer)

    defense_primary_key_to_id = {}
    defense_id_actual = 0
    for node_action_space in POMDPSettings.action_space_objects:
        for action in node_action_space:
            defense_primary_key_to_id[action.primary_key] = defense_id_actual
            defense_id_actual += 1

    write_state_transition_fast(file_pointer,defense_primary_key_to_id)
    write_observation_matrix_fast(file_pointer,defense_primary_key_to_id)
    write_rewards_fast(file_pointer,defense_primary_key_to_id)
    file_pointer.close()

def write_initial_informations(file_pointer):
    discount_line = 'discount: %s'%(POMDPSettings.DISCOUNT_FACTOR)
    value_line = 'values: reward'
    state_line = 'states: '
    states = ''
    for state in POMDPSettings.state_space:
        states = '%ss%s '%(states,state.primary_key)
    state_line = '%s%s'%(state_line,states)

    del POMDPSettings.pomdp_policy_action_index[:]
    action_line = 'actions: '
    actions = ''
    for action_type in POMDPSettings.action_space_objects:
        for action in action_type:
            actions = '%sd%s '%(actions,action.primary_key)
            POMDPSettings.pomdp_policy_action_index.append(action.primary_key)
    action_line = '%s%s' % (action_line,actions)

    observation_line = 'observations: '
    states = ''
    for state in POMDPSettings.state_space:
        states = '%so%s '%(states,state.primary_key)
    observation_line = '%s%s' % (observation_line,states)

    file_pointer.write('%s\n%s\n%s\n%s\n%s\n\n'%(discount_line,value_line,state_line,action_line,observation_line))

def write_initial_informations_fast(file_pointer):
    discount_line = 'discount: %s'%(POMDPSettings.DISCOUNT_FACTOR)
    value_line = 'values: reward'
    state_line = 'states: '
    state_line = '%s%s'%(state_line,len(POMDPSettings.state_space))

    del POMDPSettings.pomdp_policy_action_index[:]
    number_of_actions = sum([len(node_action_space) for node_action_space in POMDPSettings.action_space_objects])
    action_line = 'actions: %s'%(number_of_actions)

    observation_line = 'observations: '
    observation_line = '%s%s'%(observation_line,len(POMDPSettings.state_space))

    file_pointer.write('%s\n%s\n%s\n%s\n%s\n\n'%(discount_line,value_line,state_line,action_line,observation_line))

def write_initial_belief(file_pointer):
    POMDPSettings.current_belief.clear()
    belief_line = 'start: '
    for state in POMDPSettings.state_space:
        belief_line = '%s%s '%(belief_line,state.belief)
        POMDPSettings.current_belief[state.primary_key] = state.belief
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

def write_state_transition_fast(file_pointer,defense_primary_key_to_id):
    for defense_action_type in POMDPSettings.action_space_objects:
        for defense_action in defense_action_type:
            defense_id = defense_action.primary_key
            defense_id_pomdp = defense_primary_key_to_id[defense_action.primary_key]
            # print(POMDPSettings.state_transition_pomdp[defense_action.primary_key])
            defense_line_init = 'T: %s :' % (defense_id_pomdp)
            for old_state in POMDPSettings.state_space:
                old_state_id = old_state.primary_key
                each_old_state_to_new_state = ''
                for new_state in POMDPSettings.state_space:
                    new_state_id = new_state.primary_key
                    if new_state_id not in POMDPSettings.state_transition_pomdp[defense_id][old_state_id]:
                        continue
                    if POMDPSettings.state_transition_pomdp[defense_id][old_state_id][new_state_id]>0.0:
                        each_old_state_to_new_state = '%s :%s \t%s' % (old_state_id,new_state_id,POMDPSettings.state_transition_pomdp[defense_id][old_state_id][new_state_id])
                        defense_line = '%s%s'%(defense_line_init,each_old_state_to_new_state)
                        file_pointer.write('%s\n'%(defense_line))
    file_pointer.write('\n')

def write_observation_matrix(file_pointer):
    for action in POMDPSettings.observation_probability:
        # print(POMDPSettings.observation_probability[action])
        if action == POMDPSettings.WILDCARD_SYMBOL:
            observation_line = 'O:*\n'
        else:
            observation_line = 'O:d%s\n' % (action)
        for old_state_id in POMDPSettings.observation_probability[action]:
            each_state_to_observation = ''
            for observation in POMDPSettings.observation_probability[action][old_state_id]:
                each_state_to_observation = '%s%s ' % (each_state_to_observation,
                                                       POMDPSettings.observation_probability[action][old_state_id][
                                                           observation])
            observation_line = '%s%s\n' % (observation_line, each_state_to_observation)
        file_pointer.write('%s\n' % (observation_line))

def write_observation_matrix_fast(file_pointer,defense_primary_key_to_id):
    for action in POMDPSettings.observation_probability:
        # print(POMDPSettings.observation_probability[action])
        if action==POMDPSettings.WILDCARD_SYMBOL:
            number_of_action = len(defense_primary_key_to_id)
            for action_id in range(number_of_action):
                observation_line_init = 'O:%s :'%(action_id)
                for old_state_id in POMDPSettings.observation_probability[action]:
                    each_state_to_observation = ''
                    for observation in POMDPSettings.observation_probability[action][old_state_id]:
                        if POMDPSettings.observation_probability[action][old_state_id][observation] > 0.0:
                            each_state_to_observation = '%s :%s \t%s' % (old_state_id, observation,
                                                                         POMDPSettings.observation_probability[action][
                                                                             old_state_id][observation])
                            observation_line = '%s%s' % (observation_line_init, each_state_to_observation)
                            file_pointer.write('%s\n' % (observation_line))
            break
        else:
            action_id = defense_primary_key_to_id[action]
            observation_line_init = 'O:%s :'%(action_id)
            for old_state_id in POMDPSettings.observation_probability[action]:
                each_state_to_observation = ''
                for observation in POMDPSettings.observation_probability[action][old_state_id]:
                    if POMDPSettings.observation_probability[action][old_state_id][observation] > 0.0:
                        each_state_to_observation = '%s :%s \t%s'%(old_state_id,observation,
                                                             POMDPSettings.observation_probability[action][old_state_id][observation])
                        observation_line = '%s%s'%(observation_line_init,each_state_to_observation)
                        file_pointer.write('%s\n'%(observation_line))
    file_pointer.write('\n')

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

def write_rewards_fast(file_pointer,defense_primary_key_to_id):
    fast_rewards_pomdp = {}
    for old_state_id in POMDPSettings.rewards_pomdp:
        if old_state_id not in fast_rewards_pomdp:
            fast_rewards_pomdp[old_state_id] = {}
        for new_state_id in POMDPSettings.rewards_pomdp[old_state_id]:
            for defense_id in POMDPSettings.rewards_pomdp[old_state_id][new_state_id]:
                if defense_id not in fast_rewards_pomdp[old_state_id]:
                    fast_rewards_pomdp[old_state_id][defense_id] = 0.0
                if new_state_id in POMDPSettings.state_transition_pomdp[defense_id][old_state_id]:
                    fast_rewards_pomdp[old_state_id][defense_id] += POMDPSettings.rewards_pomdp[old_state_id][new_state_id][defense_id][POMDPSettings.WILDCARD_SYMBOL]\
                                                                    *POMDPSettings.state_transition_pomdp[defense_id][old_state_id][new_state_id]
    for old_state_id in fast_rewards_pomdp:
        for defense_id in fast_rewards_pomdp[old_state_id]:
            defense_id_pomdp_file = defense_primary_key_to_id[defense_id]
            reward_line = 'R: %s : %s : * : * %s\n'%(defense_id_pomdp_file,old_state_id,fast_rewards_pomdp[old_state_id][defense_id])
            file_pointer.write('%s'%(reward_line))