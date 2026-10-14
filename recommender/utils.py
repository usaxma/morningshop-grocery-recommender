from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "datasets"


def generateSimilarRecommendations(productToFind=1):
    productToFindSimilar = productToFind
    prod_ratings = pd.read_csv(DATA_DIR / "ratings.csv")
    product_titles = pd.read_csv(DATA_DIR / "products.csv")


    # print(prod_ratings.head())

    dataset_merge = pd.merge(prod_ratings, product_titles, on='productId')

    # print(dataset_merge.head())

    ratings = pd.DataFrame(dataset_merge.groupby('title')['rating'].mean())

    ratings['number_of_ratings'] = dataset_merge.groupby('title')['rating'].count()

    uii_matrix = dataset_merge.pivot_table(index='userId', columns='productId', values='rating')

    # print(uii_matrix.head(30))


    # print(uii_matrix.head())

    similarProd_user_rating = uii_matrix[productToFindSimilar]
    # print((melons_user_rating.head()))
    # print(ratings.sort_values('number_of_ratings',ascending=False).head(10))

    similar_to_product = uii_matrix.corrwith(similarProd_user_rating)

    relation_w_product = pd.DataFrame(similar_to_product, columns=['Correlation'])
    relation_w_product.dropna(inplace=True)

    # relation_w_product =  relation_w_product.join(ratings['number_of_ratings'])

    # print(relation_w_product.head(10))


    result = relation_w_product[relation_w_product['Correlation'] > 0.4].sort_values(by='Correlation', ascending=False)

    finalResult = result.head(10)

    data = next(finalResult.iterrows())[0]



    responseList = list()

    i = 0
    for index, row in finalResult.iterrows():

        if index != productToFindSimilar:
            # Do nothing\

            # pp.pprint(index)
            # pp.pprint(row['Correlation'])
            responseList.append({
                "product_id": index,
                "similarity": row['Correlation']
            })


    return responseList



