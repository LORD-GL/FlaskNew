def get_filtered_articles(filter_by, articles_list):
    if filter_by == 'new':
        return sorted(articles_list, key=lambda article: article.creation_date, reverse=True)
    elif filter_by == 'old':
        return sorted(articles_list, key=lambda article: article.creation_date)
    elif filter_by == 'unpopular':
        return sorted(articles_list, key=lambda article: article.views)
    elif filter_by == 'popular':
        return sorted(articles_list, key=lambda article: article.views, reverse=True)