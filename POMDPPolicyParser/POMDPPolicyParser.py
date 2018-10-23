import sys
def parse_zmdp_policy_files(file_name):
    current_vector = {}
    file_pointer = open(file_name,'r+')
    start_file_flag = False
    start_entries_flag = False
    action_entry_flag = False
    action_vector_flag = False
    current_action = None
    current_action_vector = {}
    number_of_planes = 0
    for line in file_pointer:
        line = line.replace('\n','').replace(' ','')
        if line=='' or line.startswith('#'):
            continue
        if start_file_flag and start_entries_flag:
            if '{' in line:
                action_entry_flag = True
                number_of_planes += 1
                # print(line)
                continue
            elif 'action' in line:
                if action_entry_flag:
                    current_action = int(line.split('=>')[-1].split(',')[0])
                    # print('Action <--> %s'%(current_action))
                    if current_action not in current_action_vector:
                        current_action_vector[current_action] = []
                    current_vector = {}
                    current_action_vector[current_action].append(current_vector)
                    continue
                else:
                    print(" E R R O R : Corrupted Files")
                    break
            elif '[' in line:
                if action_entry_flag:
                    action_vector_flag = True
                    continue
                else:
                    print(" E R R O R : Corrupted Files")
                    break
            elif ']' in line:
                action_vector_flag = False
                continue
            elif '}' in line:
                action_entry_flag = False
                # print('Current Actions %s --> %s'%(current_action,current_action_vector[current_action][-1]))
                continue
            elif action_entry_flag and action_vector_flag:
                # print(line)
                line = line.split(',')
                state_id = int(line[0])
                state_value = float(line[1])
                current_vector[state_id] = state_value

        elif line.startswith('{') and not start_file_flag:
            start_file_flag = True
            continue
        elif '[' in line and not start_entries_flag:
            if start_file_flag:
                start_entries_flag = True
                # print('After %s --> %s %s'%(line,start_file_flag,start_entries_flag))
                continue
            else:
                print(" E R R O R : Corrupted Files")
                break
    file_pointer.close()
    print('Number of Planes %s'%(number_of_planes))
    return current_action_vector

if __name__=='__main__':
    file_name = sys.argv[1]
    print("Name of the file %s"%(file_name))
    parse_zmdp_policy_files(file_name)

