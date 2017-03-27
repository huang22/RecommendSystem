ItemBased.py
  It is the implement of the item-based Item-based collaborative filtering.
  With "main('cosine')", the similarity is  Cosine-based Similarity.
  With "main('cosRelation')", the similarity is Correlation-based Similarity.
  With "main('pearson')", the similarity is Adjusted Cosine Similarity.

SlopeOne.py
  It is the implement of the slope one collaborative filtering.
  With "main('weights')", is Weighted Slope One.
  With "main('No')", is without weights.

MAE is a evaluation metric from "Item-Based Collaborative Filtering Recommendation Algorithms"
RMSE is root mean square error.

The two kinds of methods can predict the rating of an item in a shorttime, but the dataset is too small, so the result is not so good.
  