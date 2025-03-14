> [!NOTE]
> Hello Promtior Team!
> I tried to document my progress as I worked through the challenge and then trimmed it down to the most relevant parts - so hopefully, it’s not too long a read! Needless to say, I had a great time, and I hope you enjoy it. :)

### Initial implementation and setup
As I'm not incredibly familiar with python (or fastapi for that matter) I had to spend some time researching common language practices, project setup, and tooling. Fortunately, Python syntax is pretty intuitive, so that was a big help.

_I spent so much time_ trying to set up the project properly, my python installation was acting up and i could not get poetry to work. In the end, I just used pip with a virtual environment since it seemed like the more generic approach. I also Dockerized the app for easier deployment across different environments.

To get things started, I followed the official docs to set up a new project using langchain app new app_name. Then I copied the server example from the docs and tested the endpoints via the Playground, which turned out to be really useful. (It also auto-generates Swagger docs - very nice!)

### Building the actual app
Luckily, the rest of the process went pretty smoothly. I had been eyeing some LangChain projects before, so I had a _very rough_ idea of what I needed to do.
I looked up some docs and guides to understand how to load, transform, store and retrieve the data from the given sources. It took me a bit to figure out the overall flow of the application, but from there i was able to get it set up fairly quickly. LangChain handles a lot of the heavy lifting, so i had to read the docs and ask ChatGPT to understand some concepts and see what exactly was going on (especially when trying to understand chains and how to use them).
I also made an effort to keep the different parts of the app clearly separated. I defined:
- Loaders (for documents)
- Processors (for splitting documents and other transformations)
- Vector stores (to manage the vector DBs)
- Prompt templates and chains

I think the structure is _okay_ for the size of this project, but I’d love to see how a large-scale, production-ready app is structured.

#### Loading the documents
I first created the url loader, which i did by iterating over a list of urls until i found out about the RecursiveURLLoader., so then i used that along with bs4 to parse the documents [as shown in the docs](https://python.langchain.com/api_reference/community/document_loaders/langchain_community.document_loaders.recursive_url_loader.RecursiveUrlLoader.html).
The great thing about the RecursiveURLLoader is that it can handle nested urls, so i could just pass in the url to the challenge doc and it would load all the nested urls within it, which would be great for a larger website. 

For the challenge doc, I used the PyPDFDirectoryLoader, and loaded the data straight from the project's directory, though I would imagine the ideal place to get these type of files from is an S3/blob storage

#### Chroma vector store setup
I wasn’t entirely sure what to do with the vector DB, so for simplicity, I just generated it locally within the project's directory and let it live inside the container (without mounting a volume). Since I’m not persisting it, the embeddings get re-generated on every launch.
Chroma seemed like a popular choice, so I went with that. Later, I came across Pinecone, which looks like a really convenient, fully managed solution. The LangChain community API for it seems straightforward as well, but I didn’t get a chance to try it.
I did run into a small issue installing the Chroma dependency in the container, but adding a C++ compiler at build time fixed it.

#### Doing some tuning
The model gave me some decent responses right away, but i quickly realized the retrieved documents were not great. 
I started tweaking text splitting chunks sizes and overlaps and the retriever's searching strategy, k, k-fetch and lambda multiplier ~ This improved the results somewhat, but they still weren’t stellar. One problem was that the source **[https://www.promtior.ai/politica-de-privacidad](https://www.promtior.ai/politica-de-privacidad)** kept showing up in responses, even when it was completely irrelevant.
I researched and tried a few different approaches to improve the results:
- Several values for different parameters for the text splitter and retriever
- An [EnsembleRetriever](https://python.langchain.com/api_reference/langchain/retrievers/langchain.retrievers.ensemble.EnsembleRetriever.html) with bm25
- Parsing HTML into Markdown to preserve the markup hierarchy
- A MultiQueryRetriever 

The last one gave me _way_ better results so i stuck with it, though it naturally increased response times a bit.

The only thing i didn't get to try was a parent child retriever or treating the webpage 
documents as a separate thing (i merge both the pdf and website docs before text splitting)

I had also instructed the llm to avoid questions not in the context but it got too stubborn and was shutting down even slightly off-topic queries, so I ended up removing that restriction. 

#### Setting up a client
I thought it would be nice to have a small client app to interact with the chatbot and i was going to set up a simple frontend with React, Tailwind and Shadcn/UI.

I then looked into [assistant ui](https://www.assistant-ui.com/) which seemed quite easy to setup with Next.js. It turns out it was REALLY easy to setup - in no time i had a fully functional frontend chatbot with a clean UI. It also has markdown support, so i instructed the llm to use markdown in its replies to take full advantage of it.

I made a few small style tweaks to _somewhat_ support mobile viewports and to make the page look like something you'd find on the Promtior website. 
For deployment I used Azure Static Webapps which managed the github actions workflow for me which was nice.

#### Server deployment
Originally I tried to deploy the server straight to azure web apps but i could get it to launch the app - it was sending the zipped project fine but it would get stuck after that. So instead, I pushed my already Dockerized repo to Azure Container Registry and used that to publish a Container Web App.
I did run into some trouble with Azure credentials, but aside from that, the process wasn’t too complicated.

### Potential improvements
There are several elements of this app that could be improved and expanded upon, but just to mention a few
- Better error handling and retry/fallback mechanisms for loaders and retrievers
- Proper CORS configuration and Auth protection for the API
- Persist the VectorDB and host it somewhere -- Add methods to load, delete and update the db contents
- Provide a conversation history to the LLM for better follow up questions

### In the end 
I've been wanting to build something like this for a while, and this challenge was the perfect excuse. I’d love the chance to join the Promtior team, keep learning, and create some awesome things together. Thanks for the fun challenge!











