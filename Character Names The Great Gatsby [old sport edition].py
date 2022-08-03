# Language: Python 3
# Goal: count the names of characters in all chapters of "The Great Gatsby"
# this version counts Gatsby calling Nick "old sport" as name mentions for Nick

import os
from typing import OrderedDict
import re
import csv

# characters includes the novel's characters and the corresponding regex-patterns.
characters = OrderedDict([
    ("Nick Carraway", "Carraway house|Carraway|Mr\. Carraway|Nick|old sport"), # here the values do not contain regex groups (in parentheses) on purpose --> see explanation at special function
    ("Jay Gatsby", "Jay ?(Gatsby)?|(Mr\. )?(Jay )?Gatsby|Jimmy|(James|young) Gatz"), 
    ("Henry C. Gatz", "(Mr\.|Henry C\.) Gatz"), 
    ("Daisy Buchanan", "Daisy|Mrs\. Buchanan"), 
    ("Thomas Buchanan", "(Mr\.|Mr\. Thomas|Tom) Buchanan|Tom"), 
    ("Pammy Buchanan", "Pammy"), 
    ("Jordan Baker", "(Jordan|Miss) Baker|Jordan"), 
    ("George B. Wilson", "George Duckweed|George|George Wilson|George B\. Wilson|Mrs\. Wilson|Myrtle Wilson|Wilson"), # here the values do not contain regex groups (in parentheses) on purpose --> see explanation at special function
    ("Myrtle Wilson", "(Myrtle|Mrs.) Wilson|Myrtle"), 
    ("Catherine", "Catherine"), 
    ("Meyer Wolfshiem", "((Mr\. |Meyer )?)Wolfshiem|Meyer"), 
    ("Mavro Michaelis", "((Mavro )?)Michaelis"), 
    ("Ewing Klipspringer", "Ewing|((Mr\. )?)Klipspringer|the boarder"), 
    ("Dan Cody", "(Mr\. |Dan )?Cody"), 
    ("Lucille McKee", "Mrs\. McKee"), 
    ("Chester McKee", "Chester Beckers|Mr\. McKee|Chester"), # here the values do not contain regex groups (in parentheses) on purpose --> see explanation at special function
    ("Lucille 2", "Lucille"), 
    ("The McKees", "McKees"), 
    ("The Buchanans", "Buchanans"), 
    ("The Carraways", "Carraways"),
    ("Gilda Gray", "Gilda Gray"),
    ("Doctor T. J. Eckleburg", "Doctor (T\. J\. )?Eckleburg"),
    ("Mrs. Eberhardt", "Mrs\. Eberhardt"),
    ("Vladmir Tostoff", "Vladmir Tostoff"),
    ("Mrs. Sigourney Howard", "Mrs\. Sigourney Howard"),
    ("Nick's housekeeper", "Finn"),
    ("Owl Eyes", "Owl( E|-e)yes"),
    ("Von Hindenburg", "Von Hindenburg"),
    ("Katspaugh", "Katspaugh"),
    ("Rosy Rosenthal", "Rosy"),
    ("Ferdie", "Ferdie"),
    ("Immanuel Kant", "Kant"),
    ("Ella Kaye", "Ella"),
    ("Miss Baedeker", "Miss Baedeker"),
    ("Doctor Webster Civet", "Doc(tor)? (Webster )?Civet|Doc\W"),
    ("Blocks Biloxi", "Bill Biloxi|Biloxi"), # here the values do not contain regex groups (in parentheses) on purpose --> see explanation at special function
    ("Bill Biloxi", "Bill Biloxi"),
    ("Asa Bird", "Asa Bird"),
    ("Walter Chase", "Walter"),
    ("A pale well-dressed negro", "negro"),
    ("Stella", "Stella"),
    ("Sloane", "Sloane"),
    ("Slagle", "Slagle"),
    ("Young Parke", "Young Parke"),
    ("James J. Hill", "James J\. Hill"),
    ("Winebrenner", "Winebrenner"),
    ("the Ordways", "the Ordways"),
    ("the Herseys", "the Herseys"),
    ("the Schultzes", "the Schultzes"),
    ("the Chester Beckers", "the Chester Beckers"),
    ("the Leeches", "the Leeches"),
    ("Bunsen", "Bunsen"),
    ("the Hornbeams", "the Hornbeams"),
    ("the Willie Voltaires", "the Willie Voltaires"),
    ("the Blackbuck clan", "a whole clan named Blackbuck"),
    ("the Ismays", "the Ismays"),
    ("the Chrysties", "the Chrysties"),
    ("Hubert Auerbach", "Hubert Auerbach"),
    ("Mr. Chrystie’s wife", "Mr\. Chrystie’s wife"),
    ("Mr. Chrystie", "Mr\. Chrystie"),
    ("Edgar Beaver", "Edgar Beaver"),
    ("Clarence Endive", "Clarence Endive"),
    ("Etty", "Etty"),
    ("the Cheadles", "the Cheadles"),
    ("the O. R. P. Schraeders", "Schraeders"),
    ("the Stonewall Jackson Abrams of Georgia", "the Stonewall Jackson Abrams of Georgia"),
    ("the Fishguards", "the Fishguards"),
    ("the Rispley Snells", "the Ripley Snells"),
    ("Snell", "Snell[^s]"),
    ("Mrs. Ulysses Swett", "Mrs\. Ulysses Swett"),
    ("The Dancies", "The Dancies"),
    ("S. B. Whitebait", "S\. B\. Whitebait"),
    ("Maurice A. Flink", "Maurice A\. Flink"),
    ("the Hammerheads", "the Hammerheads"),
    ("Beluga", "Beluga[^’]"),
    ("Beluga’s girls", "Beluga’s girls"),
    ("the Poles", "the Poles"),
    ("the Mulreadys", "the Mulreadys"),
    ("Cecil Roebuck", "Cecil Roebuck"),
    ("Cecil Schoen", "Cecil Schoen"),
    ("Gulick the State senator", "Gulick the State senator"),
    ("Newton Orchid", "Newton Orchid"),
    ("Eckhaust", "Eckhaust"),
    ("Clyde Cohen", "Clyde Cohen"),
    ("Don S. Schwartz", "Don S\. Schwartz"),
    ("Arthur McCarty", "Arthur McCarty"),
    ("the Catlips", "the Catlips"),
    ("the Bembergs", "the Bembergs"),
    ("G. Earl Muldoon", "G\. Earl Muldoon"),
    ("Earl Muldoon’s brother", "that Muldoon"),
    ("Da Fontano", "Da Fontano"),
    ("Ed Legros", "Ed Legros"),
    ("James B. (“Rot-Gut”) Ferret", "Ferret"),
    ("the De Jongs", "the De Jongs"),
    ("Ernest Lilly", "Ernest Lilly"),
    ("Gus Waize", "Gus Waize"),
    ("Horace O’Donavan", "Horace O’Donavan"),
    ("Lester Myer", "Lester Myer"),
    ("George Duckweed", "George Duckweed"),
    ("Francis Bull", "Francis Bull"),
    ("the Chromes", "the Chromes"),
    ("the Backhyssons", "the Backhyssons"),
    ("the Dennickers", "the Dennickers"),
    ("Russel Betty", "Russel Betty"),
    ("the Corrigans", "the Corrigans"),
    ("the Kellehers", "the Kellehers"),
    ("the Dewars", "the Dewars"),
    ("the Scullys", "the Scullys"),
    ("S. W. Belcher", "S\. W\. Belcher"),
    ("the Smirkes", "the Smirkes"),
    ("the young Quinns", "the young Quinns"),
    ("Henry L. Palmetto", "Henry L\. Palmetto"),
    ("Benny McClenahan", "Benny McClenahan"),
    ("Faustina O’Brien", "Faustina O’Brien"),
    ("the Baedeker girls", "the Baedeker girls"),
    ("young Brewer", "young Brewer"),
    ("Mr. Albrucksburger", "Mr\. Albrucksburger"),
    ("Miss Haag", "Miss Haag"),
    ("Ardita Fitz-Peters", "Ardita Fitz-Peters"),
    ("Mr. P. Jewett", "Mr\. P\. Jewett"),
    ("Miss Claudia Hip", "Miss Claudia Hip"),
    ("Duke", "Duke[^s]"),
    ("the Dukes of Buccleuch", "the Dukes of Buccleuch")
    ])


def count_mentions(key,list_results):
    list_chapters = os.listdir()
    list_number_of_mentions = [key]
    
    for file in list_chapters:
        with open(file, encoding='utf-8') as f:
            reader = f.read()
            regex_pattern = characters[key]
            list_of_matches = re.findall(regex_pattern, reader)
            number_of_matches = len(list_of_matches)
            list_number_of_mentions.append(number_of_matches)
    list_results.append(list_number_of_mentions)

def count_mentions_Nick_Carraway(key,list_results):
    # Nick is sometimes referred to as just "Carraway", there is mentioned also "the Carraway house" which would be a false positive. Hence this special function for Nick.
    list_chapters = os.listdir()
    list_number_of_mentions = [key]
    
    for file in list_chapters:
        with open(file, encoding='utf-8') as f:
            reader = f.read()
            regex_pattern = characters[key]
            list_of_matches = re.findall(regex_pattern, reader)
            list_of_matches_fixed = []
            for match in list_of_matches:# Important! (DANGER OF FALSE POSITIVES): I avoided using groups in the regex so that list_of_matches contains all matches in full.
                if "house" not in match: # the false match is "deleted" here.
                    list_of_matches_fixed.append(match)
            if "5" in file:
                number_of_matches = len(list_of_matches_fixed)-2 # twice "old sport" does not refer to Nick in chapter 5
            elif "7" in file:
                number_of_matches = len(list_of_matches_fixed)-7 # seven times does "old sport" not refer to Nick in chapter 7
            else:
                number_of_matches = len(list_of_matches_fixed)
            list_number_of_mentions.append(number_of_matches)
    list_results.append(list_number_of_mentions)

def count_mentions_George_Wilson(key,list_results):
    # George Wilson is sometimes referred to simply as "Wilson" in the novel. I could not find a way to match "Wilson" without matching it in "Mrs. Wilson" and "Myrtle Wilson" as well. So those matches have to be deleted afterwards.
    # the novel also mentions another George, namely George Duckweed whose name is a false positive here.
    list_chapters = os.listdir()
    list_number_of_mentions = [key]
    
    for file in list_chapters:
        with open(file, encoding='utf-8') as f:
            reader = f.read()
            regex_pattern = characters[key]
            list_of_matches = re.findall(regex_pattern, reader)
            list_of_matches_fixed = []
            for match in list_of_matches: # Important! (DANGER OF FALSE POSITIVES): I avoided using groups in the regex so that list_of_matches contains all matches in full.
                if "Mrs." not in match and "Myrtle" not in match and "Duckweed" not in match: # the false matches are "deleted" here.
                    list_of_matches_fixed.append(match)
            number_of_matches = len(list_of_matches_fixed)
            list_number_of_mentions.append(number_of_matches)
    list_results.append(list_number_of_mentions)

def count_mentions_Lucille_McKee(key,list_results):
    # there is another Lucille. Lucille McKee is mentioned by her first name only once, so 1 is added to the number of matches
    list_chapters = os.listdir()
    list_number_of_mentions = [key]
    
    for file in list_chapters:
        with open(file, encoding='utf-8') as f: 
                reader = f.read()
                regex_pattern = characters[key]
                list_of_matches = re.findall(regex_pattern, reader)
                if "2" in file:
                    number_of_matches = len(list_of_matches)+1
                else:
                    number_of_matches = len(list_of_matches)
                list_number_of_mentions.append(number_of_matches)
    list_results.append(list_number_of_mentions)

def count_mentions_Chester_McKee(key,list_results):
    # the novel mentions another Chester, Chester Beckers, hence this function
    list_chapters = os.listdir()
    list_number_of_mentions = [key]
    
    for file in list_chapters:
        with open(file, encoding='utf-8') as f:
            reader = f.read()
            regex_pattern = characters[key]
            list_of_matches = re.findall(regex_pattern, reader)
            list_of_matches_fixed = []
            for match in list_of_matches:# Important! (DANGER OF FALSE POSITIVES): I avoided using groups in the regex so that list_of_matches contains all matches in full.
                if "Beckers" not in match: # the false match is "deleted" here.
                    list_of_matches_fixed.append(match)
            number_of_matches = len(list_of_matches_fixed)
            list_number_of_mentions.append(number_of_matches)
    list_results.append(list_number_of_mentions)

def count_mentions_Lucille_2(key,list_results):
    # there is another Lucille. this function fixes a false positive.
    list_chapters = os.listdir()
    list_number_of_mentions = [key]
    
    for file in list_chapters:
        with open(file, encoding='utf-8') as f: 
                reader = f.read()
                regex_pattern = characters[key]
                list_of_matches = re.findall(regex_pattern, reader)
                if "2" in file:
                    number_of_matches = len(list_of_matches)-1
                else:
                    number_of_matches = len(list_of_matches)
                list_number_of_mentions.append(number_of_matches)
    list_results.append(list_number_of_mentions)

def count_mentions_Blocks_Biloxi(key,list_results):
    # there are two Biloxis, the other is called Bill
    list_chapters = os.listdir()
    list_number_of_mentions = [key]
    
    for file in list_chapters:
        with open(file, encoding='utf-8') as f:
            reader = f.read()
            regex_pattern = characters[key]
            list_of_matches = re.findall(regex_pattern, reader)
            list_of_matches_fixed = []
            for match in list_of_matches:# Important! (DANGER OF FALSE POSITIVES): I avoided using groups in the regex so that list_of_matches contains all matches in full.
                if "Bill" not in match: # the false match is "deleted" here.
                    list_of_matches_fixed.append(match)
            number_of_matches = len(list_of_matches_fixed)
            list_number_of_mentions.append(number_of_matches)
    list_results.append(list_number_of_mentions)

def count_mentions_Tom_Buchanan(key,list_results):
    list_chapters = os.listdir()
    list_number_of_mentions = [key]
    
    for file in list_chapters:
        with open(file, encoding='utf-8') as f:
            reader = f.read()
            regex_pattern = characters[key]
            list_of_matches = re.findall(regex_pattern, reader)
            if "7" in file:
                number_of_matches = len(list_of_matches)+6 # Tom is called "old sport" six times in chapter 7
            else:
                number_of_matches = len(list_of_matches)
            list_number_of_mentions.append(number_of_matches)
    list_results.append(list_number_of_mentions)

def count_mentions_Ewing_Klipspringer(key,list_results):
    list_chapters = os.listdir()
    list_number_of_mentions = [key]
    
    for file in list_chapters:
        with open(file, encoding='utf-8') as f:
            reader = f.read()
            regex_pattern = characters[key]
            list_of_matches = re.findall(regex_pattern, reader)
            if "5" in file:
                number_of_matches = len(list_of_matches)+2 # Ewing is called "old sport" twice in chapter 5
            else:
                number_of_matches = len(list_of_matches)
            list_number_of_mentions.append(number_of_matches)
    list_results.append(list_number_of_mentions)


def write_to_csv(results):
    os.chdir(results_dir)
    rows = ["character name", "mentions in chapter 1",  "mentions in chapter 2", "mentions in chapter 3", "mentions in chapter 4", "mentions in chapter 5", "mentions in chapter 6", "mentions in chapter 7", "mentions in chapter 8", "mentions in chapter 9"]
    with open ("results_The_Great_Gatsby_[old sport edition].csv", "w") as f:
        write = csv.writer(f)
        write.writerow(rows)
        write.writerows(results)

def main():
    os.chdir(chapters_dir)
    list_chapters = os.listdir()
    list_results = []
    for key in characters.keys():
        # special function for Nick Carraway
        if key == "Nick Carraway":
            count_mentions_Nick_Carraway(key,list_results)
        
        # special function for George B. Wilson
        elif key == "George B. Wilson":
            count_mentions_George_Wilson(key,list_results)
        
        # special function for Lucille McKee
        elif key == "Lucille McKee":
           count_mentions_Lucille_McKee(key,list_results) 
       
        # special function for Chester McKee
        elif key == "Chester McKee":
           count_mentions_Chester_McKee(key,list_results) 
        
        # special function for Lucille 2 (one of the girls in yellow)
        elif key == "Lucille 2":
            count_mentions_Lucille_2(key,list_results)
        
        # special function for Blocks Biloxi
        elif key == "Blocks Biloxi":
            count_mentions_Blocks_Biloxi(key,list_results)

        # special function for Tom Buchanan
        elif key == "Thomas Buchanan":
            count_mentions_Tom_Buchanan(key,list_results)

        # special function for Ewing Klipspringer
        elif key == "Ewing Klipspringer":
            count_mentions_Ewing_Klipspringer(key,list_results)

        # the generic function for most characters
        else: 
            count_mentions(key, list_results)
        print(key,"counted")
    write_to_csv(list_results)
    print ("csv file created")
    


chapters_dir = r"C:\Users\fjbol\Desktop\Workshop Intelligent Systems\The Great Gatsby Chapters"
results_dir = r"C:\Users\fjbol\Desktop\Workshop Intelligent Systems\Results"

main()
