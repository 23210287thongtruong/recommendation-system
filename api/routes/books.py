from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
import pandas as pd
from numpy import log
import os
from joblib import load
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

router = APIRouter()


class Book(BaseModel):
    product_id: int
    title: str
    authors: str
    avg_rating: float
    n_review: int
    cover_link: str


class TrendingBook(Book):
    trending_score: float


@router.get("/trending-books", response_model=list[TrendingBook])
def get_trending_books(
    top: int = Query(10, description="Number of top trending books to return"),
):
    """
    Get the top trending books based on the rating and review count.

    :param top: Number of top trending books to return (default: 10)
    :return: List of top trending books
    """
    try:
        # Load book data from CSV
        csv_path = os.path.join(os.getcwd(), "csv", "book_data_processed.csv")
        if not os.path.exists(csv_path):
            raise HTTPException(status_code=404, detail="Book data file not found")

        df = pd.read_csv(csv_path)

        df["avg_rating"] = pd.to_numeric(df["avg_rating"], errors="coerce")
        df["n_review"] = pd.to_numeric(df["n_review"], errors="coerce")

        df = df.dropna(subset=["avg_rating", "n_review"])

        if df.empty:
            raise HTTPException(status_code=400, detail="No valid book data found")

        df["trending_score"] = df["avg_rating"] * log(1 + df["n_review"])

        trending_books = df.sort_values(by="trending_score", ascending=False).head(top)

        return [
            TrendingBook(**book) for book in trending_books.to_dict(orient="records")
        ]

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing data: {str(e)}")


@router.get("/cf-recommendations", response_model=list[Book])
def get_cf_recommendations(
    user_id: int,
    n: int = Query(5, description="Number of recommended books to return"),
):
    """
    Get book recommendations for a specific user using collaborative filtering.

    :param user_id: ID of the user to getr recommendations for
    :param n: Number of recommended books to return (default: 5)
    :return: List of recommended books
    """
    try:
        model_path = os.path.join(os.getcwd(), "svd_model.joblib")
        if not os.path.exists(model_path):
            raise HTTPException(status_code=404, detail="Model file not found")
        model_svd = load(model_path)

        data_path = os.path.join(os.getcwd(), "csv", "comments_processed.csv")
        if not os.path.exists(data_path):
            raise HTTPException(status_code=404, detail="Comments data file not found")
        cmt_cf = pd.read_csv(data_path)

        book_data_path = os.path.join(os.getcwd(), "csv", "book_data_processed.csv")
        if not os.path.exists(book_data_path):
            raise HTTPException(status_code=404, detail="Book data file not found")
        book_df = pd.read_csv(book_data_path)

        required_columns = {
            "product_id",
            "title",
            "authors",
            "avg_rating",
            "n_review",
            "cover_link",
        }
        if not required_columns.issubset(set(book_df.columns)):
            raise HTTPException(
                status_code=400, detail="Book data is missing required columns"
            )

        # Get recommendations
        all_products = cmt_cf["product_id"].unique()
        rated_products = cmt_cf[cmt_cf["customer_id"] == user_id]["product_id"].unique()
        unrated_products = [
            product for product in all_products if product not in rated_products
        ]

        predictions = [
            (product, model_svd.predict(user_id, product).est)
            for product in unrated_products
        ]
        predictions.sort(key=lambda x: x[1], reverse=True)

        recommended_books_id = [pred[0] for pred in predictions][:n]
        recommend_books_details = book_df[
            book_df["product_id"].isin(recommended_books_id)
        ].drop_duplicates(subset=["product_id"])

        return [
            Book(
                product_id=row["product_id"],
                title=row["title"],
                authors=row["authors"],
                avg_rating=row["avg_rating"],
                n_review=row["n_review"],
                cover_link=row["cover_link"],
            )
            for _, row in recommend_books_details.iterrows()
        ]

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error processing recommendations: {str(e)}"
        )


@router.get("/cbf-recommendations", response_model=list[Book])
def get_cfb_recommendations(
    product_id: int,
    n: int = Query(5, description="Number of recommended books to return"),
):
    """
    Get book recommendations using Content-Based Filtering.

    :param product_id: ID of the book to find similar recommendations for
    :param n: Number of similar books to return (default: 5)
    :return: List of recommended books with similarity scores
    """
    try:
        book_tagged_data_path = os.path.join(os.getcwd(), "csv", "book_tagged.csv")
        if not os.path.exists(book_tagged_data_path):
            raise HTTPException(status_code=404, detail="Book data file not found")

        book_data = pd.read_csv(book_tagged_data_path)

        if product_id not in book_data["product_id"].values:
            raise HTTPException(status_code=404, detail="Book ID not found in dataset")

        tfidf = TfidfVectorizer()
        tfidf_matrix = tfidf.fit_transform(book_data["tags"].fillna(""))
        content_cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

        book_index = book_data[book_data["product_id"] == product_id].index[0]

        sim_scores = list(enumerate(content_cosine_sim[book_index]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        recommended_indices = [i[0] for i in sim_scores[1 : n + 1]]
        recommended_books = book_data.iloc[recommended_indices].copy()
        recommended_books["similarity_score"] = [i[1] for i in sim_scores[1 : n + 1]]

        recommended_books = recommended_books[
            [
                "product_id",
                "title",
                "authors",
                "category",
                "avg_rating",
                "n_review",
                "similarity_score",
                "cover_link",
            ]
        ]

        return recommended_books.to_dict(orient="records")

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error processing recommendations: {str(e)}"
        )


@router.get("/hybrid-recommendations", response_model=list[dict])
def get_hybrid_recommendations(
    user_id: int = Query(..., description="User ID"),
    product_id: int = Query(..., description="Product ID"),
    n: int = Query(5, description="Number of recommendations"),
    cf_weight: float = Query(0.5, description="Weight for Collaborative Filtering"),
    cbf_weight: float = Query(0.5, description="Weight for Content-Based Filtering"),
):
    try:
        book_data_path = os.path.join(os.getcwd(), "csv", "book_data_processed.csv")

        book_data = pd.read_csv(book_data_path)

        cf_rec = get_cf_recommendations(user_id, n)
        cf_rec = pd.DataFrame([book.model_dump() for book in cf_rec])
        cf_rec["normalized_rating"] = (
            cf_rec["avg_rating"] - cf_rec["avg_rating"].min()
        ) / (cf_rec["avg_rating"].max() - cf_rec["avg_rating"].min())
        cf_rec = cf_rec[["product_id", "normalized_rating"]]

        cbf_rec = get_cfb_recommendations(product_id, n)
        cbf_rec = pd.DataFrame(cbf_rec)
        cbf_rec = cbf_rec[["product_id", "similarity_score"]]

        combined_rec = pd.merge(cf_rec, cbf_rec, on="product_id", how="outer").fillna(0)

        combined_rec["hybrid_score"] = (
            cf_weight * combined_rec["normalized_rating"]
            + cbf_weight * combined_rec["similarity_score"]
        )
        combined_rec = combined_rec.sort_values(
            by="hybrid_score", ascending=False
        ).head(n)

        recommended_books = book_data[
            book_data["product_id"].isin(combined_rec["product_id"])
        ]
        recommended_books["hybrid_score"] = recommended_books["product_id"].map(
            combined_rec.set_index("product_id")["hybrid_score"]
        )

        return recommended_books.to_dict(orient="records")

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error processing recommendations: {str(e)}"
        )
