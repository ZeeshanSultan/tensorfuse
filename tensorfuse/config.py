import os

THEANO = 0
CGT = 1
TENSORFLOW = 2
TF = 2

mode = CGT

session = None


if 'TENSORFUSE_MODE' in os.environ:
    if os.environ['TENSORFUSE_MODE'] == 'theano':
        mode = THEANO
    elif os.environ['TENSORFUSE_MODE'] == 'cgt':
        mode = CGT
    elif os.environ['TENSORFUSE_MODE'] in ['tensorflow', 'tf']:
        mode = TENSORFLOW
        import tensorflow as tf
        #_tf_config = tf.core.framework.config_pb2.ConfigProto()
        #_tf_config.inter_op_parallelism_threads = 4
        #_tf_config.intra_op_parallelism_threads = 4
        session = tf.Session()
        session.__enter__()
    else:
        raise ValueError("Unrecognized environment variable TENSORFUSE %s: must be one of 'theano', 'cgt', 'tensorflow', or 'tf'" % os.environ['TENSORFUSE_MODE'])

def is_theano():
    return mode == THEANO

def is_cgt():
    return mode == CGT

def is_tensorflow():
    return mode == TENSORFLOW

is_tf = is_tensorflow


if is_theano():
    print 'Using Theano for TensorFuse'
    import theano
    floatX = theano.config.floatX
elif is_cgt():
    print 'Using CGT for TensorFuse'
    import cgt
    floatX = cgt.floatX
else:
    print 'Using TensorFlow for TensorFuse'
    floatX = 'float32'