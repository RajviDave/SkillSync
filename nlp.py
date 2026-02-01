import numpy as np
from numpy.linalg import norm
from sentence_transformers import SentenceTransformer

sentence=["AL-ML engineer"]

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
embeddings = model.encode(sentence)
print(embeddings)

# def calculating_similarity(vec1,vec2):
#     dot_product=np.dot(vec1,vec2)

#     norm_vec1=norm(vec1)
#     norm_vec2=norm(vec2)

#     if norm_vec1==0 or norm_vec2==0:
#         return 0
    
#     similarity=dot_product/(norm_vec1*norm_vec2)
#     return similarity

# vector_a=[1,2,3,4,5]
# vector_b=[5,4,3,2,1]

# similarity_score=calculating_similarity(vector_a,vector_b)
# print(similarity_score)