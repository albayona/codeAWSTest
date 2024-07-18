import re

scraped_text = '''
{*Main scraped_text{2019 Chevrolet equinox LT Sport Utility 4D|
$9,500|
Listed |
19 hours ago|
19 hours ago|
 in |
Jeffersonville, IN|
Message|
Save|
Share|{*About this vehicle{|
Driven 134,085 miles|
Automatic transmission|
Exterior color: Black|
 |
Interior color: Black|
5/5 overall NHTSA safety rating|
5/5 front safety rating|
4/5 rollover safety rating|
5/5 side safety rating|
5/5 side barrier safety rating|
NHTSA ratings|
 |
Fuel type: |
Gasoline|
This vehicle is paid off|
Clean title|
This vehicle has no significant damage or problems.|{*Seller's description{|
 |
See less|
Jeffersonville, IN|
Location is approximate|{*Seller information{|
 |{*Seller details{|
Danny Carrillo|
(|
101|
)|
Joined Facebook in |
2008|{*Sponsored{|
 |
Reach Automotive|
Reach Automotive|
'''

sections = scraped_text.split("{")

about_list = []
seller_list = []

for index, section in enumerate(sections):
    if section.lower().startswith("*") and index + 1 < len(sections):
        about_pattern = re.compile(r'about\s*this\s*vehicle', re.IGNORECASE)
        seller_pattern1 = re.compile(r"seller's\s*description", re.IGNORECASE)
        seller_pattern2 = re.compile(r"seller\s*information", re.IGNORECASE)
        seller_pattern3 = re.compile(r"seller\s*details", re.IGNORECASE)

        index_ = sections[index + 1].replace("\n", "")
        split = index_.split("|")
        split = [item for item in split if item.strip()]

        if bool(about_pattern.search(section)):
            about_list.extend(split)

        elif bool(seller_pattern1.search(section)) or bool(seller_pattern2.search(section)) or bool(
                seller_pattern3.search(section)):
            seller_list.extend(split)

print(about_list)
print(seller_list)