import pandas as pd
import tensorflow as tf
import tensorflow_text
import tensorflow_hub as hub
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical

print('Reading input:')
df = pd.read_json('var/DataSets/664/train.json')

# Change these values if you wish to test out other dropout values
dropout_values = [0.1, 0.2, 0.5]

# Change these links if you wish to test out other versions of BERT
preprocess_url_uncased = 'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3'
preprocess_url_cased = 'https://tfhub.dev/tensorflow/bert_en_cased_preprocess/3'
encodder_url_uncased = 'https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/4'
encodder_url_cased = 'https://tfhub.dev/tensorflow/bert_en_cased_L-12_H-768_A-12/4'

print('Loading BERT:')
bert_preprocess_uncased = hub.KerasLayer(preprocess_url_uncased)
bert_encodder_uncased = hub.KerasLayer(encodder_url_uncased)
bert_preprocess_cased = hub.KerasLayer(preprocess_url_cased)
bert_encodder_cased = hub.KerasLayer(encodder_url_cased)


# There is a total of 6 combinations of hyperparameters tested
for i in range(6):
    X_train, X_test, y_train, y_test = train_test_split(df[['title','body']].agg('. '.join, axis=1), df['label'], test_size = 0.2)

    d = dropout_values[i%3]
    print(f'Run {i}: ' + ('Uncased' if i < 3 else 'Cased') + f', dropout :{d}')

    # Converts labels to one-hot vectors
    y_train = to_categorical(y_train)
    y_test = to_categorical(y_test)

    def get_sentence_embedding(sentences):
        preprossed_text = bert_preprocess_uncased(sentences) if i < 3 else bert_preprocess_cased(sentences)
        return_val = bert_encodder_uncased(preprossed_text) if i < 3 else bert_encodder_cased(preprossed_text)
        return return_val['pooled_output']

    text_input = tf.keras.layers.Input(shape=(), dtype=tf.string, name='text')
    layer = tf.keras.layers.Dropout(d, name='dropout')(get_sentence_embedding(text_input))
    layer = tf.keras.layers.Dense(3, activation='softmax', name='output')(layer)

    model = tf.keras.Model(inputs =[text_input], outputs = [layer])
    model.compile(optimizer='adam', loss = 'categorical_crossentropy', metrics=['accuracy'])# Other Optimizers can be used
    

    # Trains the model
    model.fit(X_train, y_train, epochs=5, batch_size=64)
    model.save(f'var/Scripts/664/Models/{i}')

    # This records the validation loss & accuracy (even though its called test accuracy)
    loss, accuracy = model.evaluate(X_test, y_test)

    # Writes the output results to a file
    parameter_file = open(f'var/Scripts/664/Results/{i}.txt', 'w')
    parameter_file.write(f'Dropout: {d}\n')
    parameter_file.write(f'Accuracy: {accuracy}, Loss: {loss}\n')
    parameter_file.close()
