# <img src="logo.png" alt="Search&Answer Logo" width="25"/> Search&Answer <img src="logo.png" alt="Search&Answer Logo" width="25"/>

## Figure
![Search Screen with Quick LLM Answer and Better Results](/assets/TikTok_Search_Page.jpg)
*Figure 1: Search Screen with Quick LLM Answer and Better Results*

## Inspiration
Our team loves making existing features of the app better using machine learning models and generative AI. As frequent users of TikTok, we started off by identifying the biggest pain points of the app we personally face, and then brainstorming on what we can do to fix this issue.

An increasingly popular use of TikTok has been to query as a replacement for search engines, for queries such as “best food in Singapore”, as TikTok has the added benefit of being able to see the answers in video format. However, we felt that the search feature usually did not give us optimal results when we were trying to figure out the answer to a question, so we decided to work on improving this aspect of TikTok's search feature.

We also recognised that TikTok can be used in an educational manner, as it is much easier to digest information that is presented in the short video format. If we improve the search function of the app, many users could potentially switch from using search engines to using TikTok to get quick answers or video tutorials for their questions.

## What it does
Firstly, when the user enters a query into the search box, a machine learning model is used to identify whether the query is a question or not. If it is a question, a large language model is used to generate a concise answer to the question.

Secondly, search results have their video content analysed and matched to the question and AI-generated response semantically in order to get better video search results. We video caption the videos, then use a transformer-based embedding model to embed both the video caption as well as the question and AI-generated response. The videos that correspond to the best answer to the question and AI-generated response are then recommended. 

Using this technique, we observe a large improvement in search results. Previously, video results of the search often did not answer the question but touch on some other topic related to the subject that was being searched. For example, the search “how to win a hackathon” previously recommended videos of vlogs, hackathon promotion videos, and funny videos on hackathons. With the addition of our feature, the question and AI-generated response to it had a high similarity score to videos giving advice, tips, or tricks on winning hackathons, which directly addresses the question that was asked.

## How we built it
For the first part identifying questions, we trained a support vector machine (SVM) with a radial basis function (RBF) kernel on datasets of questions and non-question queries. Cross-validation was done on the training data and the regularisation and kernel coefficient hyperparameters were tuned. 

We chose a SVM with a nonlinear kernel because identifying whether a sentence is a question seems to have a non-linear decision boundary. For example, some questions have question words, while others don't. Some sentences also have subject-verb inversion that implies that it is a question (eg. are you okay?). Hence, it seems like there can be a convincing hyperplane that serves as a decision boundary for this classification task. The task was also not too complex to the point where we had to train a neural network to capture the complexities of the data.

For the AI-generated response, we used OpenAI’s API to call for the response to the query once it is entered into the search bar. For this purpose, TikTok may choose to train their own large language model (LLM), as independent students like us don't have the resources to build our own LLM.

For the next part, there are many open-source pre-trained video captioning models available to be used, such as mPLUG2 or Salesforce’s BLIP2. While we attempted to use these models to video caption for the search results, we lacked the processing power to run these models on our local machine, and the processing power needed exceeds the limit for free online runtimes. Hence, for the purpose of this hackathon’s demo, we used an open source audio-transcribing model by OpenAI called Whisper in conjunction with image-transcribing models in order to transcribe the videos. 

The data obtained from video captioning was then concatenated with the video’s metadata, such as the user-inputed captions and hashtags. Distilbert, a popular pre-trained transformer-based embedding model, was then used to embed the video’s data as well as the question and response by the LLM. A match was done by finding videos with data having the highest cosine similarity to the question and response by the LLM, as the texts are embedded based on semantic meaning. This allows us to capture the meaning behind the question based on its vector embedding, rather than just matching the keywords and recommending videos related to, but not answering, the question.

The front-end was developed using React and Vite, which allowed us to create a responsive and interactive search interface where users can input their queries. 
For deploying our application, we used Vercel to host our main website due to its free plans and ease of use. We also considered using Vercel to host our FastAPI server, but we encountered issues with size limits on serverless functions, leading us to pivot to Render. 

## Challenges we ran into
We had a lot of issues with deployment due to the serverless size limits, which our dependencies already exceeded. We wanted to utilise AWS Lambda but faced problems with a specific module causing errors during deployment.

We had trouble finding video data for us to use to test and demo our application and new search function. We tried looking through the TikTok API but were ultimately still unable to find any relevant ones that would have streamlined our development process.

Due to our limitations and computational power and disk space, many methods we wanted to try were out of the question, such as using existing pre-trained open source video captioning models or training our own video analysis models (video data is way too huge for us to handle). We were also unable to tune our hyperparameters for the SVM well, despite running it overnight on our MacBook.

## Accomplishments that we're proud of
We are particularly proud of our ability to overcome various technical limitations and deployment challenges to deliver a fully functional prototype. With our limited resources, we managed to get 3 different machine learning models to work in a short time for our purpose, linked with our front-end buttons. We also managed to work around our resource limitation to find the next best solution after the existing state of the art methods that we may not have access to, such as running GridSearchCV overnight on a virtual machine for hyperparameter tuning instead of HPO algorithms, and combining audio transcription models with image transcription instead of video captioning models.

We are very proud of the result of our combination of these models, as we found that the search gave us much better results after our changes to it. Of the top 5 results, at least 4 videos will answer the question directly, compared to approximately 1 in 4 previously. With our simple proof of concept, we believe that TikTok has the resources available to execute our improvements to the search function with even better models, eliminating a huge pain point of the app and providing a much better user experience.

Our models also fare quite well in production, which you can test on our live website! 

## What we learned
We learned how to choose the type of machine learning models to solve real-world issues, keeping in mind constraints such as computational power, time taken for the model to load, size of the model for serverless deployment, etc. We also got to put our front-end and model deployment skills to use, during which we learned a lot about the whole full-stack experience of machine learning, from idea conception to   back-end and front-end coding to deployment.

## What's next for Search&Answer
We hope that we will be able to collaborate with TikTok to gain access to more robust datasets and computational resources, enabling us to implement more sophisticated video captioning models.

We also aim to leverage more powerful machine learning models to enhance performance and accuracy. This was a challenge for us during development due to our limited computational resources.
