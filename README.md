Vote predictor
==============

Saying our current political climate is in turmoil is a gross understatement. We are deliberately bombarded with data so that we lose sight of what is important. This is why it is important to use statistical analysis to act as a guiding light in our search for the relevant.

__Vote predictor__ is a statistical model that attempts to predict how lawmakers vote. Lawmakers follow certain patterns when voting. These patterns exist because lawmakers should to the best of their ability follow what their constituents want. The purpose of this tool is to raise a flag indicating that a lawmaker is voting differently than expected. This change in behavior might happen for many different reasons, the author of this tool hopes the user will look more into what might have caused their deviation. Since this model uses logistic regression the predicted probabilities could also serve as an indicator telling us which lawmakers are more likely to be swayed to vote a different way informing the people to contact them in case they want to change their lawmaker's mind. 

The model uses Latent Dirichlet Allocation (LDA) which describes the bills as a distribution of the topics within them. The Congressional Research Services take the task to label and categorize every bill. I made sure that there were at least 20 bills per topic to ensure that every topic was sufficiently represented in my data set. After cleaning the text and making the corpus I ran LDA to identify 55 hidden topics within them. This resulted in each bill being represented by 55 numbers that add up to one. I used these 55 variables to train one logistic regression model per lawmaker that used the passage votes for each bill that they have voted on as the response variable.

Results here?
