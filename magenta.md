# magenta项目记录

- 环境安装：

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

  - 

  