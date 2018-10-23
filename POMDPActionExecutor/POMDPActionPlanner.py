import sys,math
from POMDPPolicyParser import POMDPPolicyParser
from POMDPActionExecutor import ActionProperties
import POMDPSettings

def find_optimal_action(policy,belief):
    ''' This functions enumerates all the generated linear functions and
    chooses the action with the maximum value'''
    max_value = None
    action_index = None
    for action in policy:
        execute_action = policy[action]
        for alpha_vector in execute_action:
            current_value = 0.0
            for state_portion in belief:
                if belief[state_portion] == 0:
                    continue
                if state_portion not in alpha_vector:
                    break
                current_value += alpha_vector[state_portion]*belief[state_portion]
            if max_value is None or max_value < current_value:
                max_value = current_value
                action_index = action
    # print("Recommended Action %s"%(action_index))
    return action_index

def execute_action(belief):
    # belief = {i:0.0 for i in range(8)}
    # for i in range(4):
    #     belief[i] += 1.0 / 5
    # print(sum([len(i) for i in POMDPSettings.action_space_objects]))
    # print(len(POMDPSettings.state_space))
    return find_optimal_action(ActionProperties.pomdp_policies, belief)

def get_policy_functions(file_name):
    ActionProperties.pomdp_policies = POMDPPolicyParser.parse_zmdp_policy_files(file_name)
    # ActionProperties.print_POMDP_policies(ActionProperties.pomdp_policies)

if __name__=='__main__':
    file_name = sys.argv[1]
    print("Name of the file %s"%(file_name))
    ActionProperties.pomdp_policies = POMDPPolicyParser.parse_zmdp_policy_files(file_name)
    belief = {}
    for i in range(8):
        belief[i] = 1.0/8
    ActionProperties.print_POMDP_policies(ActionProperties.pomdp_policies)
    find_optimal_action(ActionProperties.pomdp_policies,belief)