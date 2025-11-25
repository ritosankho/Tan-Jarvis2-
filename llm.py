from llama_cpp import Llama
from queues import log_queue

# Path to the GGUF model
def run_llm(prompt, model_path):

    llm = Llama(
        model_path=model_path,
        verbose = False,
        n_ctx=4096,           # context window (you can reduce to 2048)
        n_threads=4,          # your Ryzen 7 7730U has 8 cores
        n_batch=128,          # batch size (speed vs RAM)
        n_gpu_layers=20

        #chat_format="auto",
    )


    output = llm(
        prompt,
        max_tokens=400,
        temperature=0.9,
        top_p=0.9
    )

    return (output["choices"][0]["text"])
