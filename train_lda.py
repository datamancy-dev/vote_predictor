from sklearn.decomposition import LatentDirichletAllocation


NUM_TOPICS = 30


LDA = LatentDirichletAllocation(n_components=NUM_TOPICS, learning_method='online', )

