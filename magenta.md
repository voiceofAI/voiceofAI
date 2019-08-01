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
  # 或者
  HPARAMS="label_smoothing=0.0,max_length=0,max_target_seq_length=2048"
  t2t_trainer --t2t_usr_dir=s2p  --data_dir=input   --hparams=${HPARAMS}  --hparams_set=score2perf_transformer_base   --model=transformer  --output_dir=input/training/dir  --problem=s2p_local   --train_steps=100
  ```

  > 参考<https://github.com/voiceofAI/tensor2tensor/blob/master/docs/new_model.md>

  ```bash
	# 报错的大问题！！！！！！！！！！已经处理
tensorflow.python.framework.errors_impl.InvalidArgumentError: input tensor must have non-zero dims. Found: [420, 0, 0, 3].
	# 解决方法：hparams没传进去，不建议用\来分行
	```

- <https://github.com/tensorflow/magenta/issues/1491>

- 生成

  ```bash
  # 交互式生成，在交互式窗口中填写前置midi文件名或留空（即随机生成）
  HPARAMS_SET=score2perf_transformer_base
  MODEL=transformer
  PROBLEM=s2p_local
  
  DECODE_HPARAMS="alpha=0,beam_size=1,extra_length=2048"
  
  t2t_decoder   --t2t_usr_dir=s2p --data_dir=input   --decode_hparams="${DECODE_HPARAMS}"   --decode_interactive   --hparams="sampling_method=random"   --hparams_set=${HPARAMS_SET}   --model=${MODEL}   --problem=${PROBLEM}   --output_dir=input/training/dir
  
  # 交互式命令
  #INTERACTIVE MODE  num_samples=1  decode_length=2048
  #  it=<input_type>     ('text' or 'image' or 'label', default: text)
  #  ns=<num_samples>    (changes number of samples, default: 1)
  #  dl=<decode_length>  (changes decode length, default: 100)
  #  <target_prefix>                (decode)
  #  q                   (quit)
  #>little_init.midi
  ```

  ```bash
  # 也可以用encode_file
  HPARAMS_SET=score2perf_transformer_base
  MODEL=transformer
  PROBLEM=s2p_local
  
  DECODE_HPARAMS="alpha=0,beam_size=1,extra_length=2048"
  
  t2t_decoder   --t2t_usr_dir=s2p --data_dir=input   --decode_hparams="${DECODE_HPARAMS}"         --hparams_set=${HPARAMS_SET}   --model=${MODEL}   --problem=${PROBLEM}   --output_dir=input/training/dir    --decode_from_file=start.txt --decode_to_file=output.txt
  
  # start.txt里面：
  # little_init.midi
  # output.txt里面：
  # /tmp/tmpn6h7w_u1_decode.mid
  ```

  





- 可视化工具：https://github.com/tensorflow/magenta/issues/1498
- <https://github.com/tensorflow/tensor2tensor/issues/420>
- <https://github.com/tensorflow/tensor2tensor/blob/master/tensor2tensor/visualization/TransformerVisualization.ipynb>