import requests
from google_img_source_search import ReverseImageSearcher

def testar():
    #if __name__ == '__main__':
    #image_url = 'https://i.pinimg.com/originals/c4/50/35/c450352ac6ea8645ead206721673e8fb.png'
    image_url = 'https://stsci-opo.org/STScI-01G77PKYA4T05YKJ3EDQ36NZCX.png'
    #image_url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Ana_de_armas_%2852409484768%29_%28cropped%29.jpg/375px-Ana_de_armas_%2852409484768%29_%28cropped%29.jpg'

    rev_img_searcher = ReverseImageSearcher()
    res = rev_img_searcher.search(image_url)

    for search_item in res:
        print(f'Title: {search_item.page_title}')
        print(f'Site: {search_item.page_url}')
        print(f'Img: {search_item.image_url}\n')
        
def procurarImagem(image_url):
    #if __name__ == '__main__':
    #image_url = 'https://i.pinimg.com/originals/c4/50/35/c450352ac6ea8645ead206721673e8fb.png'

    rev_img_searcher = ReverseImageSearcher()
    res = rev_img_searcher.search(image_url)

    return res
    # for search_item in res:
    #     print(f'Title: {search_item.page_title}')
    #     print(f'Site: {search_item.page_url}')
    #     print(f'Img: {search_item.image_url}\n')        