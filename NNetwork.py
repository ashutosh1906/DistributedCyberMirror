import tensorflow as tf
import random
import numpy as np

knowledge_database = []
attack_list = {0:'nnr',1:'nr',2:'f',3:'fs'}
def __run_neural_network(knowledge_dataset,cross_validation_enabled=False,
                       num_cv_interation = 1,
                         cv_train_ratio=1):
    NUMBER_ATTRIBUTE = len(knowledge_dataset[0])
    num_data_row_size = NUMBER_ATTRIBUTE-1
    num_label_size = len(attack_list)

    #################### Neural Network Model Parameters##########################
    learning_rate = 0.01
    epochs = 200
    batch_size = 30
    #################### End Neural Network Model Parameters##########################

    ######################### Declare TF Variables for feeding Dataset#############################
    ####################### 1.1 Feeding Dataset ############################
    input_conditions = tf.placeholder(tf.float32, [None, num_data_row_size])
    input_probabilities = tf.placeholder(tf.float32, [None, num_label_size])

    ##################### 1.2.1 Prepare First Layer #################################################
    hidden_layer1_node = num_data_row_size
    ##################### 1.2.2 Declare First Layer Input Variables #################################################
    weight_input_layer1 = tf.Variable(tf.random_normal([num_data_row_size, hidden_layer1_node], stddev=0.03),
                                      name='weight_input_layer1')
    weight_bias_layer1 = tf.Variable(tf.random_normal([hidden_layer1_node]),
                                     name='weight_bias_layer1')

    ######################### 1.2.2 Declare First Layer Output Variables  #############################################
    weight_output_layer1 = tf.Variable(tf.random_normal([hidden_layer1_node, num_label_size], stddev=0.03),
                                      name='weight_output_layer1')
    weight_output_bias_layer1 = tf.Variable(tf.random_normal([num_label_size]),
                                     name='weight_output_bias_layer1')

    ####################### 1.3 Define Co-relations #############################################
    axon_value_layer1 = tf.add(tf.matmul(input_conditions, weight_input_layer1), weight_bias_layer1)
    axon_value_layer1 = tf.nn.relu(axon_value_layer1)

    ###################### 1.4 Predict the probability ############################################
    predicted_prob = tf.nn.softmax(
        tf.add(tf.matmul(axon_value_layer1, weight_output_layer1),weight_output_bias_layer1))  ##### normalize the vector into a probabilitic distribution ######
    predicted_prob_clipped = tf.clip_by_value(predicted_prob, 1e-10, 0.9999999)

    ###################### 1.5 Build the Neural Network ############################################
    cross_entropy = -tf.reduce_mean(tf.reduce_sum(input_probabilities * tf.log(predicted_prob_clipped)
                                                  + (1 - input_probabilities) * tf.log(1 - predicted_prob_clipped), axis=1))
    optimiser = tf.train.GradientDescentOptimizer(learning_rate=learning_rate).minimize(cross_entropy)
    prediction_error = tf.reduce_mean(tf.sqrt(tf.reduce_sum
                                              (tf.square(predicted_prob_clipped - input_probabilities))))

    init_op = tf.global_variables_initializer()
    ################################## Fetch the dataset ###############################################
    if not cross_validation_enabled:
        num_cv_interation = 1
        cv_train_ratio = 1.00

    with tf.Session() as sess:
        # initialise the variables
        best_model_Saver = tf.train.Saver()
        sess.run(init_op)
        best_model_based_entropy = 100000.0 ##### Infinite value
        best_model_cv = 100000.0 ##### Infinite value
        for cv_index in range(num_cv_interation):
            if cv_train_ratio < 1:
                random.shuffle(knowledge_dataset)
            train_data_size = int(cv_train_ratio * len(knowledge_dataset))-1
            cv_test_data_size = len(knowledge_dataset) - train_data_size
            train_data = np.zeros(shape=(train_data_size,num_data_row_size), dtype=int)
            train_data_label = np.zeros(shape=(train_data_size,num_label_size))
            for i in range(train_data_size):
                for j in range(NUMBER_ATTRIBUTE - 1):
                    train_data[i][j] = knowledge_dataset[i][j]
                    # print('%s %s'%(train_data[i][j],Properties.knowledge_database[i][j]))
                print('Test Label %s' % (knowledge_dataset[i][NUMBER_ATTRIBUTE - 1]))
                for k in range(num_label_size):
                    train_data_label[i][k] = knowledge_dataset[i][NUMBER_ATTRIBUTE - 1][k]

            # ######################## check for train data ######################
            # column = ['State at (t-1)', 'State at (t-2)',
            #           'Attack at (t-2)', 'Defense at (t-1)', 'Defense at (t-2)']
            # global check_df
            # check_df = pf.DataFrame(train_data,columns=column)
            # #
            # ######################## check for train data label ######################
            # column_label = ['prob_%s'%(i) for i in range(total_number_attack_action)]
            # global check_df_label
            # check_df_label = pf.DataFrame(train_data_label,columns=column_label)

            cv_test_data = np.zeros(shape=(cv_test_data_size,num_data_row_size), dtype=int)
            cv_test_data_label = np.zeros(shape=(cv_test_data_size,num_label_size))

            for i in range(cv_test_data_size):
                for j in range(NUMBER_ATTRIBUTE - 1):
                    cv_test_data[i][j] = knowledge_dataset[train_data_size + i][j]
                # for k in range(num_label_size):
                #     cv_test_data_label[i][k] = knowledge_dataset[train_data_size + i][NUMBER_ATTRIBUTE - 1][k]

            # ######################## check for train data ######################
            # column = ['State at (t-1)', 'State at (t-2)',
            #           'Attack at (t-2)', 'Defense at (t-1)', 'Defense at (t-2)']
            # global check_df
            # check_df = pf.DataFrame(cv_test_data,columns=column)
            #
            ######################## check for train data label ######################

            # ######################## check for train data label ######################
            # column_label = ['prob_%s' % (i) for i in range(total_number_attack_action)]
            # global check_df_label
            # check_df_label = pf.DataFrame(cv_test_data_label, columns=column_label)

            print('Build Neural Network %s' % (cv_index))

            total_batch = int((train_data_size - 1) / batch_size) + 1
            for epoch in range(epochs):
                avg_cost = 0.0
                for i in range(total_batch):
                    batch_start = i * batch_size
                    batch_x = train_data[batch_start:(batch_start + batch_size)]
                    batch_y = train_data_label[batch_start:(batch_start + batch_size)]
                    _, c = sess.run([optimiser, cross_entropy],
                                    feed_dict={input_conditions: batch_x, input_probabilities: batch_y})
                    avg_cost += c  # / total_batch
                # print("Epoch:", (epoch + 1), "cost =", "{:.5f}".format(avg_cost))


                if cross_validation_enabled:
                    if cv_test_data_size > 0:
                        p_error = sess.run(prediction_error, feed_dict=
                        {input_conditions: np.reshape(cv_test_data, (cv_test_data_size, num_data_row_size)),
                         input_probabilities: np.reshape(cv_test_data_label, (cv_test_data_size, num_label_size))})

                        print("Prediction Error %s"%(p_error))
                        # if (cv_index == 0 and epoch == 0) or best_model_cv > p_error:
                        #     best_model_cv = p_error
                        #     save_path = best_model_Saver.save(sess,ConfigurationPOMDPGenerator.NEURAL_NETWORK_MODEL_SAVER_PATH)
                        #     # print("Cross Validation : Save the model of epoch index %s --> %s" % (epoch,save_path))
                    continue

                if (cv_index == 0 and epoch ==0) or best_model_based_entropy > avg_cost:
                    # print("Save the model of epoch index %s"%(epoch))
                    best_model_based_entropy = avg_cost
            print(sess.run(predicted_prob_clipped,
                           feed_dict={input_conditions: np.reshape(cv_test_data[-1], (1, num_data_row_size))}))
            # if not cross_validation_enabled:
            #     save_path = best_model_Saver.save(sess,ConfigurationPOMDPGenerator.NEURAL_NETWORK_MODEL_SAVER_PATH)
            #     # print("Saved the model in %s" % (save_path))

def knowledge_database_print():
    print('$$$$$$ Knowledge Database $$$$$$$$$$$$$$$$$$')
    for i in range(len(knowledge_database)):
        print(knowledge_database[i])

def write_database():
    file_pointer = open('knowledge_database','w')
    for i in knowledge_database:
        write_line = ''
        for j in range(len(i)):
            if j==0:
                write_line = i[j]
                continue
            write_line = '%s;%s'%(write_line,i[j])
        file_pointer.write('%s\n'%(write_line))
    file_pointer.close()

if __name__=='__main__':
    print('Attack Prediction Model using Neural Network')

    file_pointer = open('knowledge_database','r+')
    for line in file_pointer:
        attr_list = line.replace('\n','').split(';')
        datarow = []
        # print(attr_list)
        for i in range(len(attr_list)-1):
            datarow.append(float(attr_list[i]))
        attr_list[len(attr_list)-1] = attr_list[len(attr_list)-1].replace('[','').replace(']','').split(',')
        attack_prob = []
        for j in range(len(attr_list[len(attr_list)-1])):
            attack_prob.append(float(attr_list[len(attr_list)-1][j]))
        datarow.append(attack_prob)
        # print(datarow)
        knowledge_database.append(datarow)
    file_pointer.close()

    knowledge_database_print()
    while(True):
        con_flag = int(input("Press 0 to exit  "))
        if con_flag:
            print("Input current condition:")
            proximity_value = int(input("Proximity Value = "))
            scanning_interval = float(input("Scannin Interval = "))
            advancing_interval = float(input("Advancing Interval = "))
            failure_probability = float(input("Failure Probability = "))
            current_data_row = [proximity_value, scanning_interval, advancing_interval, failure_probability,
                                []]
            knowledge_database.append(current_data_row)
            print("Current Data %s" % (current_data_row))

            __run_neural_network(knowledge_database)

            print("Input the Previous Observations:")
            adv_action_prob = [0.0 for i in range(len(attack_list))]
            adv_action = int(input("Adversary Action ID = "))
            adv_action_prob[adv_action] = 1.0

            # print("Current Data %s"% (current_data_row))
            knowledge_database[-1][len(knowledge_database[-1])-1] = adv_action_prob
            # print_kd()
        else:
            break

    write_database()










