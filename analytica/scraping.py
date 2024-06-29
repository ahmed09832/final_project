import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup


def get_html_content(asin, page_num=1):
    proxy_params = {
      'api_key': '7b79551e-7fe0-4def-8254-c45bb8b4dc78',
      'url': f'https://www.amazon.com/product-reviews/{asin}/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber={page_num}', 
      'render_js': True,
      }

    response = requests.get(
      url='https://proxy.scrapeops.io/v1/',
      params= urlencode(proxy_params),
      timeout=120,
    )
    
    return response


def extract_review_title(review_tag):
    title = review_tag.find('a', attrs={"data-hook": "review-title"}).find_all('span')[-1].text.strip()
    return title


def extract_review_body(review_tag):
    text = review_tag.find('span', attrs={"data-hook": "review-body"}).find('span').text.strip()
    return text




def get_data(review_tag):
    return extract_review_title(review_tag) + ' ' + extract_review_body(review_tag)



# def get_reviews(asin):
#     reviews_data = []
#     page_num = 1
#     while True: 
#         response = get_html_content(asin=asin, page_num=page_num)
#         soup = BeautifulSoup(response.content, 'html.parser')

#         review_tags = soup.find_all('div', attrs={"data-hook": "review"})

#         if len(review_tags) == 0:
#             break
#         else:
#             for review_tag in review_tags:
#                 review = get_data(review_tag)
#                 reviews_data.append(review)
#         page_num+=1
        
#     return reviews_data


revs = ['This product so far has not disappointed. My children love to use it and I like the ability to monitor control what content they see with ease.',
 'great for beginner or experienced person. Bought as a gift and she loves it',
 'Inexpensive tablet for him to use and learn on, step up from the NABI. He was thrilled with it, learn how to Skype on it already...',
 "I've had my Fire HD 8 two weeks now and I love it. This tablet is a great value.We are Prime Members and that is where this tablet SHINES. I love being able to easily access all of the Prime content as well as movies you can download and watch laterThis has a 1280/800 screen which has some really nice look to it its nice and crisp and very bright infact it is brighter then the ipad pro costing $900 base model. The build on this fire is INSANELY AWESOME running at only 7.7mm thick and the smooth glossy feel on the back it is really amazing to hold its like the futuristic tab in ur hands.",
 'I bought this for my grand daughter when she comes over to visit. I set it up with her as the user, entered her age and name and now Amazon makes sure that she only accesses sites and content that are appropriate to her age. Simple to do and she loves the capabilities. I also bought and installed a 64gig SD card which gives this little tablet plenty of storage. For the price I think this tablet is best one out there. You can spend hundreds of dollars more for additional speed and capacity but when it comes to the basics this tablets does everything that most people will ever need at a fraction of the cost.',
 'This amazon fire 8 inch tablet is the perfect size. I purchased it for my husband so that he has a bigger screen than just his phone. He had gotten me one a few years ago so I knew it would be a good purchase.',
 'Great for e-reading on the go, nice and light weight, and for the price point given, definitely worth the purchase.',
 'I gave this as a Christmas gift to my inlaws, husband and uncle. They loved it and how easy they are to use with fantastic features!',
 'Great as a device to read books. I like that it links with my borrowed library e-books. Switched from another popular tablet brand and I am happy with the choice I made. It took some time to get books from my previous non-Kindle reader, but finally figured out a way!',
 'I love ordering books and reading them with the reader.',
 'this is negative reviews and this s very bad reviews ',
 'ths product is not good',
 'the product is very very bad',
 'One of the PD ports only charges at regular speeds.', 
 "The charges a 60W only from one USB-C port. They advertise dual 60 W USB-C ports, but it does not matter if you only use one of the USB-C ports or both at the same time. I only got this one over the other ones that cost less because of the ability to charge two items at 60 W simultaneously. With this charge, I can only do it from only one port. The other three ports work but at a slower rate. Stay away from this charger.",
 "I bought this because I had something I wanted to plug in along with my two phones so I need a 3 ports. However I still have to use my old car charger because this one you have to wiggle your USB charger around to even get it to start working and then if you bump it it stops charging your stuff and you have to wiggle around the court again The innards are loose in the court itself not the USB cords. So essentially I bought it and it doesn't work.",
 "Doesn't have ports that light up as advertised. Can't see where to put the cord in a dark vehicle other than that works well."]




def get_reviews(asin):
    return revs
