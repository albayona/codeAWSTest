import traceback
from api.DTOs.SimplePost import SimplePost
from api.models import Post


def get_simple_post_max_tag(soup):
    tags = soup.find_all(['a'])

    classes = {}

    for tag in tags:
        cList = tag['class']
        key = ""
        for c in cList:
            key += " " + c

        if classes.get(key) is None:
            classes[key] = 0
        else:
            classes[key] += 1

    max_class = ""
    max_class_cont = 0

    for c in classes:
        if c != "" and max_class_cont < classes[c]:
            max_class = c

    print('maxtag')
    print(max_class)
    return max_class[1:]



def get_all_simple_posts(soup, tag):
    all_posts = soup.find_all('a', tag)
    atrs = []
    for p in all_posts:
        try:
            link_parts = p['href'].split('/')
            attributes = SimplePost(
                link=link_parts[3]
            )

            atrs.append(attributes)
        except:
            traceback.print_exc()
            pass

    return atrs


def non_existent(simple_post):
    return not Post.objects.filter(link=simple_post.link).exists()

def create_post(simple_post):
    return Post.objects.create(link=simple_post.link)