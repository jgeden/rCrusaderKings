import praw
import tweepy
import requests
import time
import config

def reddit_login():
	try:
		reddit = praw.Reddit(client_id=config.client_id, 
							 client_secret=config.client_secret, 
							 user_agent=config.user_agent)
		return reddit
	except:
		print('Login failed')

# downloads an image from a url into images/<title>.jpg
def get_image(url):
	with open('img.jpg', 'wb') as image:
		response = requests.get(url, stream=True)

		if not response.ok:
			print(response)
		else:
			image.write(response.content)
			image.close()

def post_tweet(title, img_path):
	auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_key_secret)
	auth.set_access_token(config.access_token, config.access_token_secret)

	api = tweepy.API(auth)

	try:
		api.verify_credentials()
		print('Auth ok')

		api.update_with_media(img_path, title)
		print('Posted!')
	except:
		print('Error during auth')

def main():
	# login to reddit
	reddit = reddit_login()

	# get past posts
	previous_posts = []
	previous_posts_file = open('previous_posts.txt', 'r')
	posts = previous_posts_file.readlines()
	for post in posts:
		previous_posts.append(post)
	previous_posts_file.close()

	# get top 10 current hottest posts
	for submission in reddit.subreddit('CrusaderKings').hot(limit=10):
		if not submission.stickied:
			# format the tweet title
			title = str(submission.title) + ' #CrusaderKings'
			title += '\nposted by u/' + str(submission.author)
			title += ' ' + str('redd.it/' + str(submission))

			# check if the post has an image
			if '.png' in submission.url or '.jpg' in submission.url:
				print('//////////////////////////////////')
				print(title)
				print('//////////////////////////////////\n')
				
				if (str(submission.title) + '\n') not in previous_posts:
					# get the image from the post
					get_image(submission.url)

					# post the tweet
					post_tweet(title, 'img.jpg')

					outfile = open('previous_posts.txt', 'a')
					outfile.write(str(submission.title) + '\n')
					outfile.close()
				
					time.sleep(5)
				else:
					print('Duplicate post')


if __name__ == '__main__':
	main()