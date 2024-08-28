from src.gmaps import Gmaps



queries = [
   "clubs in pune"
]

Gmaps.places(queries,max=5)