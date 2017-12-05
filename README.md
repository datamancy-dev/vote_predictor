## Vote predictor

----

Saying our current political climate is in turmoil is a gross understatement. We are deliberately bombarded with data so that we lose sight of what is important. This is why it is important to use statistical analysis to act as a guiding light in our search for the relevant.

__Vote predictor__ is a statistical model loosely based on the [model](http://www.cs.columbia.edu/~blei/papers/GerrishBlei2012.pdf) by Gerrish and Blei. The model attempts to predict how lawmakers will vote given bill text data. Lawmakers follow certain patterns when voting. These patterns exist because lawmakers should to the best of their ability follow what their constituents want. The purpose of this tool is to raise a flag indicating that a lawmaker is voting differently than expected. This change in behavior might happen for many different reasons, the author of this tool hopes the user will look more into what might have caused their deviation. Since this model uses logistic regression the predicted probabilities could also serve as an indicator telling us which lawmakers are more likely to be swayed to vote a different way informing the people to contact them in case they want to change their lawmaker's mind. 

The model uses Latent Dirichlet Allocation (LDA) which describes the bills as a distribution of the topics within them. The Congressional Research Services take the task to label and categorize every bill. I made sure that there were at least 20 bills per topic to ensure that every topic was sufficiently represented in my data set. After cleaning the text and making the corpus I ran LDA to identify 55 hidden topics within them. This resulted in each bill being represented by 55 numbers that add up to one. I used these 55 variables to train one logistic regression model per lawmaker that used the passage votes for each bill that they have voted on as the response variable.

### Logistic Regression Results
----
My results were measured with cross validated accuracy. These are the ranges of accuracy I got (histogram coming soon)
|Chamber|Min|Max|Avg|
|-|-|-|-|
|Senate|.46|.97|.8|
|House|.53|.99|.77|

A few notes about these:
- Since there is a model per lawmaker and some lawmakers have voted on very few bills these models tend to be overfit since my ratio of samples to independent variables is nearly 1:1
- The average accuracy models however have an average ratio of 4:1 making them slightly better but still unstable models
- This is a major flaw in the design of the model. Possible solutions for this could include:
    - Running a likelihood ratio test to decrease the amount of independent variables.
    - Decreasing the number of topics found by LDA (essentially reducing the amount of independent variables in a different way)
    - Redesigning the model to be one model per congress session. This also yields for more interesting features to look at like what party had the house majority during that congress.


### LDA Results
---
Not all topics found by LDA made sense and there was a bit of redundancy between them. However most of the topics were sensical. These are just a few examples of some topics' top ten stemmed words

|Topic: Immigration| Topic: Infrastructure| Topic: Defense|
|-|-|-|
|patent|rail|air forc|
|immigr nation|bridg|navi|
|nation act|rout|nation guard|
|immigr nation act|corridor|defense committe|
|imprison|freight|test evalu|
|petition|ca|congression defense|
|invent|railroad|war terror|
|trial|street|delet sec|
|visa|metropolitan|congression defens committe|
|nonimmigr|amtrak|sec fund appropri|

---
More information about the lawmakers and bills used is available in the datasets directory of this project.
More information about how I obtained these results is available in the src directory of this project.
