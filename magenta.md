# magenta项目记录

> by zkcpku

## 环境安装：

- 安装在win10下的ubuntu子系统中，已提前安装**anaconda**和**gcc**

- <https://github.com/voiceofAI/magenta#using-magenta>

- 安装时注意修改python版本<https://github.com/tensorflow/magenta/issues/1477>

- 安装`rtmidi`失败，可尝试`sudo apt-get install build-essential libasound2-dev libjack-dev`，以及更新apt源 `sudo apt-get update`，并再次安装`pip install magenta`

- 运行中 报错关于`soundfile`（`snf`），<<https://pypi.org/project/SoundFile/>>，可以`sudo apt-get install libsndfile1`

  > In a modern Python, you can use `pip install soundfile` to download and install the latest release of SoundFile and its dependencies. On Windows and OS X, this will also install the library libsndfile. On Linux, you need to install libsndfile using your distribution’s package manager, for example `sudo apt-get install libsndfile1`.

- demo尝试

  - Create NoteSequences：

    ```bash
    INPUT_DIRECTORY=<folder containing MIDI and/or MusicXML files. can have child folders.>
    
    # TFRecord file that will contain NoteSequence protocol buffers.
    SEQUENCES_TFRECORD=/tmp/notesequences.tfrecord
    
    convert_dir_to_note_sequences \
      --input_dir=$INPUT_DIRECTORY \
      --output_file=$SEQUENCES_TFRECORD \
      --recursive
      
    
    # 比如
    convert_dir_to_note_sequences --input_dir=midi_data  --output_file=input/notesequences.tfrecord  --recursive
    ```

  - Create SequenceExamples

    ```bash
    melody_rnn_create_dataset 
    --config=attention_rnn
    --input=tmp/notesequences.tfrecord
    --output_dir=tmp/sequence_examples
    --eval_ratio=0.10
    # 注意删去反斜杠
    ```

  - 剩下的可按照<https://github.com/voiceofAI/magenta/tree/master/magenta/models/melody_rnn>

- pipeline分析

  > <https://github.com/voiceofAI/magenta/tree/master/magenta/pipelines>


## music transformer

- 可能有用的链接：

  - <https://github.com/tensorflow/magenta/issues?utf8=%E2%9C%93&q=score2perf>
  - <https://github.com/tensorflow/magenta/issues/1408>

- 先要生成tfrecord文件，并显式地写在s2p_local.py文件中

- 数据处理命令：

  ```bash
  t2t-datagen  --t2t_usr_dir=s2p   --data_dir=input   --problem=s2p_local   --tmp_dir=input/tmp   --alsologtostderr
  ```

  > 参考<https://github.com/voiceofAI/tensor2tensor/blob/master/docs/new_problem.md>

- 安装py2.7...以及一个加速库python-snappy和依赖：<https://cloud.tencent.com/developer/ask/51257>

- ![1564162454004](E:\pic\1564162454004.png)

- 训练命令：

  ```bash
  DATA_DIR=input
  HPARAMS_SET=score2perf_transformer_base
  MODEL=transformer
  PROBLEM=s2p_local
  TRAIN_DIR=input/training/dir
  
  HPARAMS="label_smoothing=0.0,""max_length=0,"\
  "max_target_seq_length=2048"
  t2t_trainer --t2t_usr_dir=s2p  --data_dir=input   --hparams=${HPARAMS}  --hparams_set=${HPARAMS_SET}   --model=${MODEL}  --output_dir=${TRAIN_DIR}  --problem=${PROBLEM}   --train_steps=100
  
  
  # 或者
  HPARAMS=\
  "label_smoothing=0.0,"\
  "max_length=0,"\
  "max_target_seq_length=2048"
  t2t_trainer --t2t_usr_dir=s2p  --data_dir=input   --hparams=${HPARAMS}  --hparams_set=score2perf_transformer_base   --model=transformer  --output_dir=input/training/dir  --problem=s2p_local   --train_steps=100
  ```

  > 参考<https://github.com/voiceofAI/tensor2tensor/blob/master/docs/new_model.md>

```bash
# 报错的大问题！！！！！！！！！！尚未处理
Traceback (most recent call last):
  File "/home/zkcpku/anaconda3/envs/magenta2/bin/t2t_trainer", line 10, in <module>
    sys.exit(console_entry_point())
  File "/home/zkcpku/anaconda3/envs/magenta2/lib/python2.7/site-packages/magenta/tensor2tensor/t2t_trainer.py", line 34, in console_entry_point
    tf.app.run(main)
  File "/home/zkcpku/anaconda3/envs/magenta2/lib/python2.7/site-packages/tensorflow/python/platform/app.py", line 40, in run
    _run(main=main, argv=argv, flags_parser=_parse_flags_tolerate_undef)
  File "/home/zkcpku/anaconda3/envs/magenta2/lib/python2.7/site-packages/absl/app.py", line 300, in run
    _run_main(main, args)
  File "/home/zkcpku/anaconda3/envs/magenta2/lib/python2.7/site-packages/absl/app.py", line 251, in _run_main
    sys.exit(main(argv))
  File "/home/zkcpku/anaconda3/envs/magenta2/lib/python2.7/site-packages/magenta/tensor2tensor/t2t_trainer.py", line 29, in main
    t2t_trainer.main(argv)
  File "/home/zkcpku/anaconda3/envs/magenta2/lib/python2.7/site-packages/tensor2tensor/bin/t2t_trainer.py", line 401, in main
    execute_schedule(exp)
  File "/home/zkcpku/anaconda3/envs/magenta2/lib/python2.7/site-packages/tensor2tensor/bin/t2t_trainer.py", line 356, in execute_schedule
    getattr(exp, FLAGS.schedule)()
  File "/home/zkcpku/anaconda3/envs/magenta2/lib/python2.7/site-packages/tensor2tensor/utils/trainer_lib.py", line 401, in continuous_train_and_eval
    self._eval_spec)
  File "/home/zkcpku/anaconda3/envs/magenta2/lib/python2.7/site-packages/tensorflow_estimator/python/estimator/training.py", line 473, in train_and_evaluate
    return executor.run()
  File "/home/zkcpku/anaconda3/envs/magenta2/lib/python2.7/site-packages/tensorflow_estimator/python/estimator/training.py", line 613, in run
    return self.run_local()
  File "/home/zkcpku/anaconda3/envs/magenta2/lib/python2.7/site-packages/tensorflow_estimator/python/estimator/training.py", line 714, in run_local
    saving_listeners=saving_listeners)
  File "/home/zkcpku/anaconda3/envs/magenta2/lib/python2.7/site-packages/tensorflow_estimator/python/estimator/estimator.py", line 367, in train
    loss = self._train_model(input_fn, hooks, saving_listeners)
  File "/home/zkcpku/anaconda3/envs/magenta2/lib/python2.7/site-packages/tensorflow_estimator/python/estimator/estimator.py", line 1158, in _train_model
    return self._train_model_default(input_fn, hooks, saving_listeners)
  File "/home/zkcpku/anaconda3/envs/magenta2/lib/python2.7/site-packages/tensorflow_estimator/python/estimator/estimator.py", line 1192, in _train_model_default
    saving_listeners)
  File "/home/zkcpku/anaconda3/envs/magenta2/lib/python2.7/site-packages/tensorflow_estimator/python/estimator/estimator.py", line 1484, in _train_with_estimator_spec
    _, loss = mon_sess.run([estimator_spec.train_op, estimator_spec.loss])
  File "/home/zkcpku/anaconda3/envs/magenta2/lib/python2.7/site-packages/tensorflow/python/training/monitored_session.py", line 754, in run
    run_metadata=run_metadata)
  File "/home/zkcpku/anaconda3/envs/magenta2/lib/python2.7/site-packages/tensorflow/python/training/monitored_session.py", line 1252, in run
    run_metadata=run_metadata)
  File "/home/zkcpku/anaconda3/envs/magenta2/lib/python2.7/site-packages/tensorflow/python/training/monitored_session.py", line 1353, in run
    raise six.reraise(*original_exc_info)
  File "/home/zkcpku/anaconda3/envs/magenta2/lib/python2.7/site-packages/tensorflow/python/training/monitored_session.py", line 1338, in run
    return self._sess.run(*args, **kwargs)
  File "/home/zkcpku/anaconda3/envs/magenta2/lib/python2.7/site-packages/tensorflow/python/training/monitored_session.py", line 1411, in run
    run_metadata=run_metadata)
  File "/home/zkcpku/anaconda3/envs/magenta2/lib/python2.7/site-packages/tensorflow/python/training/monitored_session.py", line 1169, in run
    return self._sess.run(*args, **kwargs)
  File "/home/zkcpku/anaconda3/envs/magenta2/lib/python2.7/site-packages/tensorflow/python/client/session.py", line 950, in run
    run_metadata_ptr)
  File "/home/zkcpku/anaconda3/envs/magenta2/lib/python2.7/site-packages/tensorflow/python/client/session.py", line 1173, in _run
    feed_dict_tensor, options, run_metadata)
  File "/home/zkcpku/anaconda3/envs/magenta2/lib/python2.7/site-packages/tensorflow/python/client/session.py", line 1350, in _do_run
    run_metadata)
  File "/home/zkcpku/anaconda3/envs/magenta2/lib/python2.7/site-packages/tensorflow/python/client/session.py", line 1370, in _do_call
    raise type(e)(node_def, op, message)
tensorflow.python.framework.errors_impl.InvalidArgumentError: input tensor must have non-zero dims. Found: [420, 0, 0, 3].
```

- <https://github.com/tensorflow/magenta/issues/1491>

- 生成

  ```bash
  DECODE_HPARAMS="alpha=0,beam_size=1,extra_length=2048"
  
  t2t_decoder  --t2t_usr_dir=s2p  --data_dir=input  --decode_hparams="${DECODE_HPARAMS}"   --decode_interactive   --hparams="sampling_method=random"   --hparams_set=score2perf_transformer_base   --model=transformer --problem=s2p_local   --output_dir=output
  
  ```

  





- 可视化工具：https://github.com/tensorflow/magenta/issues/1498
- <https://github.com/tensorflow/tensor2tensor/issues/420>
- <https://github.com/tensorflow/tensor2tensor/blob/master/tensor2tensor/visualization/TransformerVisualization.ipynb>