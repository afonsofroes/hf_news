import requests

"""
This module gathers the trending models, datasets and posts from Hugging Face's website. All the information gathered is
returned in a dictionary, trend_data.
The dictionary is structured as follows:
    models: list of raw outputs from the API for trending models, very rich in information
    datasets: list of raw outputs from the API for trending datasets, very rich in information
    posts: list of trending post information. Preprocessed to only include the content, date of publication and author.
"""


def get_trending_models_and_datasets():
    trends = ["model", "dataset"]
    trending_models_and_datasets = {}
    for trend in trends:
        url = f"https://huggingface.co/api/trending?type={trend}"
        response = requests.get(url).json()
        trending_models_and_datasets[f"{trend}s"] = response

    return trending_models_and_datasets


def get_trending_posts():
    url = f"https://huggingface.co/api/posts?sort=trending"

    response = requests.get(url).json()

    # reconstruct post from response
    trending_posts = []

    posts = response["socialPosts"]
    for post in posts:
        content = "".join([line["raw"] for line in post["content"]])

        post_with_details = {}
        post_with_details["content"] = content
        post_with_details["publishedAt"] = post["publishedAt"].split("T")[0]
        post_with_details["author"] = post["author"]["name"]
        trending_posts.append(post_with_details)

    return trending_posts


def get_hf_trends():
    # aggregate data
    trend_data = get_trending_models_and_datasets()
    trending_posts = get_trending_posts()
    trend_data["posts"] = trending_posts

    return trend_data
