import random


class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

   @staticmethod
   def rand():
      colors = ["PURPLE", "CYAN", "DARKCYAN", "BLUE", "YELLOW"]

      return getattr(color, colors[random.randrange(0, len(colors))])