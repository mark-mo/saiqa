########
# Code based on https://github.com/Steven-Hewitt/QA-with-Tensorflow/blob/master/QA%20with%20Tensorflow.ipynb
# Cleaned by Mark Mott
#
# This class runs a single instance of the Dynamic Memory Network architecture over a question and its relavent data
########

batch_size = 0 # <- Change to how much data was returned based on the question
limit = 5
logits = 0 # Pull from a saved object
corrbool = 0 # Pull from saved object
total_loss = 0 # Pull from saved object
attends=0#?

final_test_data = finalize(test_data) # TODO: Replace with data relavent to the question

# The number of dimensions used to store data passed between recurrent layers in the network.
recurrent_cell_size = 128

# Dropout probabilities
input_p = 0.5

# How many questions we train on at a time
batch_size = 128 # Change

# Context: A [batch_size, maximum_context_length, word_vectorization_dimensions] tensor
# that contains all the context information.
context = tf.placeholder(tf.float32, [None, None, D], "context")
context_placeholder = context  # I use context as a variable name later on

# input_sentence_endings: A [batch_size, maximum_sentence_count, 2] tensor that
# contains the locations of the ends of sentences.
input_sentence_endings = tf.placeholder(tf.int32, [None, None, 2], "sentence")

# recurrent_cell_size: the number of hidden units in recurrent layers.
input_gru = tf.contrib.rnn.GRUCell(recurrent_cell_size)

# input_p: The probability of maintaining a specific hidden input unit.
# Likewise, output_p is the probability of maintaining a specific hidden output unit.
gru_drop = tf.contrib.rnn.DropoutWrapper(input_gru, input_p, output_p)

# dynamic_rnn also returns the final internal state. We don't need that, and can
# ignore the corresponding output (_).
input_module_outputs, _ = tf.nn.dynamic_rnn(gru_drop, context, dtype=tf.float32, scope="input_module")

# cs: the facts gathered from the context.
cs = tf.gather_nd(input_module_outputs, input_sentence_endings)

# query: A [batch_size, maximum_question_length, word_vectorization_dimensions] tensor
#  that contains all of the questions.
query = tf.placeholder(tf.float32, [None, None, D], "query")

# input_query_lengths: A [batch_size, 2] tensor that contains question length information.
# input_query_lengths[:,1] has the actual lengths; input_query_lengths[:,0] is a simple range()
# so that it plays nice with gather_nd.
input_query_lengths = tf.placeholder(tf.int32, [None, 2], "query_lengths")

question_module_outputs, _ = tf.nn.dynamic_rnn(gru_drop, query, dtype=tf.float32,
                                               scope=tf.VariableScope(True, "input_module"))

# q: the question states. A [batch_size, recurrent_cell_size] tensor.
q = tf.gather_nd(question_module_outputs, input_query_lengths)

# make sure the current memory (i.e. the question vector) is broadcasted along the facts dimension
size = tf.stack([tf.constant(1), tf.shape(cs)[1], tf.constant(1)])

# locs: A boolean tensor that indicates where the score
#  matches the minimum score. This happens on multiple dimensions,
#  so in the off chance there's one or two indexes that match
#  we make sure it matches in all indexes.
logloc = tf.reduce_max(logits, -1, keep_dims=True)
locs = tf.equal(logits, logloc)

# facts_0s: a [batch_size, max_facts_length, 1] tensor
#     whose values are 1 if the corresponding fact exists and 0 if not.
facts_0s = tf.cast(tf.count_nonzero(input_sentence_endings[:, :, -1:], -1, keep_dims=True), tf.float32)

# Prepare validation set
batch = np.random.randint(final_test_data.shape[0], size=batch_size * 10)
batch_data = final_test_data[batch]

# def prep_data(batch_data) # Might be able to save the result

validation_set, val_context_words, val_cqas = prep_batch(batch_data, True)

# Run the GRU architecture
ancr = sess.run([corrbool, locs, total_loss, logits, facts_0s, w_1] + attends +
                [query, cs, question_module_outputs], feed_dict=validation_set)

# Get results from the model
n = ancr[1]

validation_set, val_context_words, val_cqas = prep_batch(batch_data, True)

# Locations of responses within contexts
indices = np.argmax(n, axis=1)

# Output the answer
# TODO: Remove for loop, only need to run once/only one answer
for i, cw in list(zip(indices, val_context_words))[:limit]:
    cw[i]