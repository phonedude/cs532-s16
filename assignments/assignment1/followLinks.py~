from bs4 import BeautifulSoup
import requests

def get_frontier(alist):
    frontier = []
    pdf = []
    for a in alist:
        if '.pdf' not in a['href']:
            frontier.append(a['href'])
        else:
            pdf .append(a['href'])
    return (frontier,pdf)



def decend_once(frontier,onceFromOnce=False):
    for front in frontier:
        r = requests.get(front)
        print(r.headers)




if __name__ == '__main__':
    request = requests.get("http://www.cs.odu.edu/~mln/teaching/cs532-s16/test/pdfs.html")
    print(request.headers)
    print(request.text)
    soup = BeautifulSoup(request.text,'html5lib')
    all_a = soup.find_all('a',href=True)
    seen = set()
    potential_pdf = get_frontier(all_a)

    for not_pdf in potential_pdf[0]:
        print(not_pdf)
        r = requests.get(not_pdf)
        print(r.headers)
        print(r.headers['Content-type'])
    print("____________________________")
    for pdf in potential_pdf[1]:
        print(pdf)
        r = requests.get(pdf)
        print(r.headers)
        print(r.headers['Content-type'])


