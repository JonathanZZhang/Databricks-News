import torch
from transformers import pipeline
from langchain.llms import HuggingFacePipeline
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document

device = 0 if torch.cuda.is_available() else -1  # 0 is the device number for the first GPU

generate_text = pipeline(task="summarization", 
                        #  model="facebook/bart-large-cnn", 
                        model = "ainize/bart-base-cnn",
                        # model = "google/pegasus-cnn_dailymail",
                         torch_dtype=torch.bfloat16,
                         trust_remote_code=True, 
                         device=device)  # explicitly set the device here
# print(device)

# We are using Hugging Face's transformers library, which provides a high-level API for various tasks 
# like text generation, summarization, translation, etc. The HuggingFacePipeline class is a wrapper 
# that makes it easy to use these features.

hf_pipeline = HuggingFacePipeline(pipeline=generate_text)

# The summarize_chain is a sequence of transformations that will be applied to the input text to 
# generate a summary. This might involve various steps such as tokenization, applying the model, and 
# post-processing the output. We're loading a pre-defined chain that has been tuned for the task of 
# refining summaries.

summarize_chain = load_summarize_chain(hf_pipeline, chain_type="refine")

def summarize(content):
    text_splitter = CharacterTextSplitter()
    texts = text_splitter.split_text(content)
    docs = [Document(page_content=t) for t in texts]
    
    return summarize_chain.run(docs)
