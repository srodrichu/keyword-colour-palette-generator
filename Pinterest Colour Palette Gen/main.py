import pinterestspider
import ColourPalette
from ColourPalette import DominantColours
from pinterestspider import PinterestScraper

def main(username, password, keyword):

	ps = pinterestspider.PinterestScraper(username,password,keyword)

	arr = ps.main()

	ColourPalette.accaPlot(arr,5)

if __name__ == '__main__':

	username = input("Pinterest Username: ")
	password = input("Password: ")
	keyword = input("Input your keyword: ")

	main(username, password, keyword)
