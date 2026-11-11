from src.parser import ForumParser
from config import DEFAULT_URL
from src.database import DatabaseRepository
from src.loader import PageLoader

repository = DatabaseRepository()
loader = PageLoader()
parser = ForumParser()

url = DEFAULT_URL

if __name__ == '__main__':
    parser.parse_page(url)