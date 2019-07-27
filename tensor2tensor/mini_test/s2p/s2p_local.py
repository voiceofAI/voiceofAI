from magenta.models.score2perf.score2perf import *

LOCAL_TFRECORD_PATHS = {
    'train': 'input/train.tfrecord',
    'dev': 'input/dev.tfrecord',
    'test': 'input/test.tfrecord'
}


@registry.register_problem('s2p_local')
class s2p_local(Score2PerfProblem):
  """Piano performance language model on the MAESTRO dataset."""

  def performances_input_transform(self, tmp_dir):
    del tmp_dir
    return dict(
        (split_name, datagen_beam.ReadNoteSequencesFromTFRecord(tfrecord_path))
        for split_name, tfrecord_path in LOCAL_TFRECORD_PATHS.items())

  @property
  def splits(self):
    return None

  @property
  def min_hop_size_seconds(self):
    return 0.0

  @property
  def max_hop_size_seconds(self):
    return 0.0

  @property
  def add_eos_symbol(self):
    return False

  @property
  def stretch_factors(self):
    # Stretch by -5%, -2.5%, 0%, 2.5%, and 5%.
    return [0.95, 0.975, 1.0, 1.025, 1.05]

  @property
  def transpose_amounts(self):
    # Transpose no more than a minor third.
    return [-3, -2, -1, 0, 1, 2, 3]

  @property
  def random_crop_in_train(self):
    return True

  @property
  def split_in_eval(self):
    return True