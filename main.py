from post_analysis import PostAnalysis
from account import Account


username = "danbilzerian"
user = Account(username)
user.load_full_page()
posts = user.get_posts()

for each_post in posts:
    post = PostAnalysis(each_post)
    post.load_full_page()
    comments = post.get_comments()
    comment_text = post.get_comment_text(comments)
    print("Sentiment_Analysis for " + each_post + " : " +
          post.get_sentiment(comment_text))


# post = PostAnalysis("https://www.instagram.com/p/BwWvMLZAl1Y/")
# post.load_full_page()
# comments = post.get_comments()
# comment_text = post.get_comment_text(comments)
# print("Sentiment_Analysis for https://www.instagram.com/p/BwWvMLZAl1Y/ : " +
#       post.get_sentiment(comment_text))
