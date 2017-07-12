import numpy as np
import tensorflow as tf
from periodictable import elements
from scipy.spatial import distance

filename = 'train.sdf'
startstr = "  -OEChem"

# Read entire file and parse into list of strings
with open(filename, 'r') as f:
    data = f.readlines()
# print( '{:d} {:s}'.format(len(data), ' lines read' ) )

def get_batch():
    train_data_dists = []
    train_data_connects = []
    # Search for the beginning of each block of Atoms in file and get the index
    for idx, line in enumerate(data) :
        if startstr in line :
            # Store line 4 from each block into a list
            temp = data[idx + 2].split()
            # Store atom count
            atmcount = temp[0]
            if int(atmcount) > 28:
                # print("Skipping this molecule")
                continue
            n = len(atmcount)
            # Scenario if atom count is greater than 999
            if n > 3 :
                numxyz = int(atmcount[0:n/2])
                numc = int(atmcount[n/2:n])
            else :
                numxyz = int(temp[0])
                numc = int(temp[1])

            xyz = [[0.0 for i in range(3)] for j in range (numxyz)]
            connect = [[0 for i in range(3)] for j in range(numc)]
            atmnum = np.zeros(shape=(28,1))
            connection_table = np.zeros(shape=(28,28))
            distance_table = np.zeros(shape=(28,29))

            for i in range(numxyz) :
                temp = data[idx + 3 + i].split()
                # Loop through periodic table to find element number for each symbol and store it
                for el in elements :
                    if temp[3] == el.symbol :
                        atmnum[i] = float(el.number)
                for j in range(3) :
                    xyz[i][j] = float(temp[j])

            for a in range(numxyz):
                distance_table[a][0] = float(atmnum[a])

            for l in range(numxyz):
                for i in range(numxyz):
                    distance_table[l][i + 1] = distance.euclidean(xyz[l], xyz[i])

            train_data_dists.append([distance_table.flatten()])

            for i in range(numc) :
                temp = data[idx + 3 + i + numxyz].split()
                if len(temp) == 2 :
                    atmcount = temp[0]
                    n = len(atmcount)
                    connect[i][0] = int(atmcount[0:n/2])
                    connect[i][1] = int(atmcount[n/2:n])
                    connect[i][2] = int(temp[1])
                else :
                    connect[i][0] = int(temp[0])
                    connect[i][1] = int(temp[1])
                    connect[i][2] = int(temp[2])
            # Record connection information in the connection table of all Atoms in molecule
            for i in range(numc):
                connection_table[connect[i][0] - 1][connect[i][1] - 1] = 1.0
                connection_table[connect[i][1] - 1][connect[i][0] - 1] = 1.0

#            atmnum.shape = (28, 1)
#            connection_table_final = np.hstack((atmnum, connection_table))
            train_data_connects.append([connection_table.flatten()])

    return train_data_dists, train_data_connects

# x will be the input matrix flattened (28x29)
x = tf.placeholder(tf.float32, [None, 812])

# Define the weights (initial value doesn't matter since these will be learned)
# W = tf.Variable(tf.random_uniform([812, 812], minval=0, dtype=tf.float32))
W1 = tf.Variable(tf.truncated_normal([812, 784], stddev=0.1))
b1 = tf.Variable(tf.truncated_normal([784], stddev=0.1))
W2 = tf.Variable(tf.truncated_normal([784, 784], stddev=0.1))
b2 = tf.Variable(tf.truncated_normal([784], stddev=0.1))
W3 = tf.Variable(tf.truncated_normal([784, 784], stddev=0.1))
b3 = tf.Variable(tf.truncated_normal([784], stddev=0.1))
W = tf.Variable(tf.truncated_normal([784, 784], stddev=0.1))
b = tf.Variable(tf.truncated_normal([784], stddev=0.1))

# Predict output matrix
# y = tf.nn.softmax(tf.nn.l2_normalize(tf.matmul(x, W) + b, dim= 0, epsilon=1e-12))
# y = tf.nn.sigmoid(tf.matmul(x, W) + b)
# y = tf.nn.relu(tf.nn.sigmoid(tf.matmul(x, W) + b))
layer1 = tf.add(tf.matmul(x, W1), b1)
layer1 = tf.nn.relu(layer1)

layer2 = tf.add(tf.matmul(layer1, W2), b2)
layer2 = tf.nn.relu(layer2)

layer3 = tf.add(tf.matmul(layer2, W3), b3)
layer3 = tf.nn.relu(layer3)

y = tf.add(tf.matmul(layer3, W), b)
y = tf.nn.sigmoid(y)

# Actual output matrix from the training set
y_ = tf.placeholder(tf.float32, [None, 784])

# Calculate loss and optimize
cross_entropy = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(labels=y_, logits=y))
# cross_entropy = tf.reduce_sum(tf.abs(y - y_))
train_step = tf.train.AdamOptimizer(0.001).minimize(cross_entropy)

sess = tf.InteractiveSession()
tf.global_variables_initializer().run()

a, b = get_batch()
train_len = len(a)

correct_prediction = tf.equal(y_, y)
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

# Training
for i in range(train_len):
    batch_xs = a[i]
    batch_ys = b[i]
    _, loss, acc = sess.run([train_step, cross_entropy, accuracy], feed_dict={x: batch_xs, y_: batch_ys})
    print("Loss= " + "{:.6f}".format(loss) + " Accuracy= " + "{:.5f}".format(acc))
    print(batch_ys)
    print(y.eval({x: batch_xs}))

# Test trained model
cumulative_accuracy = 0.0
for i in range(train_len):
    acc_batch_xs = a[i]
    acc_batch_ys = b[i]
    cumulative_accuracy += accuracy.eval(feed_dict={x: acc_batch_xs, y_: acc_batch_ys})
print("Test Accuracy= {}".format(cumulative_accuracy / train_len))
