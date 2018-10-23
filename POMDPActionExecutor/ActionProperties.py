########################### Properties of Policy #########################
pomdp_policies = None

###################### Print Policies #######################
def print_POMDP_policies(policy):
    print('************* Print Policies *************')
    for action in policy:
        print('Action is %s'%(action))
        execute_action = policy[action]
        for alpha_vector in execute_action:
            print('\t Start of new plane (Action = %s)'%(action))
            for state_portion in alpha_vector:
                print('\t\t State %s --> %s'%(state_portion,alpha_vector[state_portion]))
    print('*********** End of printing policies ****************')