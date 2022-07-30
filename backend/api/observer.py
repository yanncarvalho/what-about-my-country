class ObserverDB :

  def save (self):
      from backend.populate_db import Populate
      Populate().start()


