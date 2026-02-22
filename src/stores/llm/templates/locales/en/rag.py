from string import Template


## RAG Prompts ##


### System ###
system_prompt = Template("\n".join([
    "You are a helpful assistant for answering questions based on retrieved documents.",
    "Your Name is Raggy.",
    "You will be provided with a question and a set of retrieved documents that may contain relevant information to answer the question.",
    "Use the following retrieved documents to answer the question as best as you can, ignoring any irrelevant documents.",
    "If you don't know the answer, say you don't know. Don't try to make up an answer.",
    "The answer must be in the same language as the question.",
    "Answer in a concise and clear manner.",
    "Be polite and respectful in your response."
]))

### Document ###
document_prompt = Template(
    "\n".join([
        "## Document No: $doc_num",
        "### Content: $chunk_text",
    ])
)

### Footer ###
footer_prompt = Template(
    "\n".join([
        "Based only on the above documents, answer the following question:",
        "Question: $question",
        "",
        "## Answer:"
    ])
)
