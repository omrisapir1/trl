from datasets import load_dataset, Dataset
import pandas as pd
from trl import GRPOTrainer, GRPOConfig
import random


df = pd.read_pickle('/Users/omri.sapir/learning/math_kaggle/SECOT_MATH/data/15K_TRPO_trainset.pkl')[['problem','numerical_solution']]

hf_dataset = Dataset.from_pandas(df, preserve_index=False)


# dataset = load_dataset("trl-lib/tldr", split="train")
# dataset = dataset.filter(lambda x: random.random() < 0.0001)
# Dummy reward function: count the number of unique caracteres in the completions
def reward_num_unique_chars(completions, **kwargs):
    return [len(set(c)) for c in completions]

training_args = GRPOConfig(output_dir="Qwen2-0.5B-GRPO", use_vllm=True)


trainer = GRPOTrainer(
    model="Qwen/Qwen2-0.5B-Instruct",
    reward_funcs=reward_num_unique_chars,
    train_dataset=hf_dataset,
    args=training_args,
)
trainer.train()